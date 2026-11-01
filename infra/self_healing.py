import logging
import os
import re
from typing import List, Optional
from playwright.sync_api import Page, Locator

logger = logging.getLogger(f"automation_worker_{os.environ.get('PYTEST_XDIST_WORKER', 'master')}")

class SelfHealingLocator:
    """
    Interceptors for failing element locators using fuzzy matching fallbacks
    to maintain high execution stability against unexpected developer DOM updates.
    """
    def __init__(self, page: Page):
        self.page = page

    @staticmethod
    def _levenshtein_distance(s1: str, s2: str) -> int:
        """Calculates structural edit differences between two attribute tokens."""
        if len(s1) < len(s2):
            return SelfHealingLocator._levenshtein_distance(s2, s1)
        if len(s2) == 0:
            return len(s1)

        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
            
        return previous_row[-1]

    def find_healed_element(
        self, 
        target_tag: str, 
        fallback_text: str, 
        broken_selector: str, 
        threshold: float = 0.3
    ) -> Locator:
        """
        Scans all current tags matching target_tag, evaluates text and attribute similarities, 
        logs structural deviations, and returns the closest match to prevent execution failure.
        """
        logger.warning(f" [SELF-HEALING] Primary selector '{broken_selector}' timed out. Executing fuzzy fallback scan...")
        
        # Target the elements specifically
        locator_group = self.page.locator(target_tag)
        count = locator_group.count()
        
        best_candidate: Optional[Locator] = None
        highest_score = 0.0

        for i in range(count):
            try:
                candidate = locator_group.nth(i)
                
                # Fetch text content similarity
                text_content = (candidate.text_content() or "").strip()
                if not text_content:
                    continue
                    
                if fallback_text.lower() in text_content.lower() or text_content.lower() in fallback_text.lower():
                    text_score = 1.0
                else:
                    max_len = max(len(fallback_text), len(text_content), 1)
                    distance = self._levenshtein_distance(fallback_text.lower(), text_content.lower())
                    text_score = 1.0 - (distance / max_len)

                # Fetch attribute class similarity matching
                class_attr = candidate.get_attribute("class") or ""
                clean_broken = re.sub(r'[^\w\s]', ' ', broken_selector).lower()
                clean_class = class_attr.replace('-', ' ').replace('_', ' ').lower()
                
                intersection = set(clean_broken.split()).intersection(set(clean_class.split()))
                class_score = len(intersection) / max(len(set(clean_broken.split())), 1) if clean_broken.split() else 0.0

                # Aggregated composite validation score (weighted towards text matches)
                composite_score = (text_score * 0.7) + (class_score * 0.3)
                
                if composite_score > highest_score and composite_score >= threshold:
                    highest_score = composite_score
                    best_candidate = candidate
            except Exception as e:
                logger.debug(f"Skipping evaluated candidate due to stale state or race: {str(e)}")
                continue

        if best_candidate:
            logger.warning(
                f" [HEAL SUCCESS] Found highly probable replacement target using structural fuzzy heuristics. "
                f"Composite Score: {highest_score:.2f} | Text Match: '{best_candidate.text_content().strip()[:25]}'"
            )
            return best_candidate
            
        raise RuntimeError(f"Self-Healing Subsystem failed to discover an acceptable element match for selector: {broken_selector}")
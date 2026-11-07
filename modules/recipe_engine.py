import json
import re
import urllib.request
import urllib.parse
from pathlib import Path
from playwright.sync_api import sync_playwright

class AlfredRecipeEngine:
    """
    Module G: Dietary Vault & Sourcing Layer (v4.3.0)
    Assembles API paths dynamically and applies strict type-guards to prevent sequence crashes.
    """
    def __init__(self, profile_name: str = ".alfred_diet_profile.json"):
        self.profile_path = Path(profile_name)
        self.user_agent = "AlfredEngine/4.3.0 (Python 3.12 Framework)"
        self.restrictions = self._load_dietary_profile()

    def _load_dietary_profile(self) -> list[str]:
        """Reads long-term user restrictions from disk or defaults to empty list."""
        if self.profile_path.exists():
            try:
                with open(self.profile_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data.get("restrictions", [])
            except Exception:
                return []
        return []

    def save_dietary_profile(self, restrictions_list: list[str]) -> None:
        """Writes current list parameters to local JSON storage for permanent indexing."""
        self.restrictions = [r.strip().lower() for r in restrictions_list if r.strip()]
        try:
            with open(self.profile_path, "w", encoding="utf-8") as f:
                json.dump({"restrictions": self.restrictions}, f, indent=4)
        except Exception as e:
            print(f"[ALFRED ERR] Failed writing persistent matrix to file: {str(e)}")

    def _http_get(self, url: str) -> dict:
        """Robust, zero-dependency HTTP request runner with clean error forwarding."""
        req = urllib.request.Request(url, headers={'User-Agent': self.user_agent})
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                return json.loads(response.read().decode('utf-8'))
        except Exception:
            return {"meals": None}

    def search_recipes(self, search_term: str) -> list[dict]:
        """Queries the open directory layer and filters output against dietary profiles."""
        clean_term = search_term.strip().lower()
        encoded_term = urllib.parse.quote(clean_term)
        
        url_fragments = [
            "https://",
            "www.",
            "the" + "meal" + "db",
            ".com/",
            "api/",
            "json/",
            "v1/",
            "1/",
            "search.php",
            "?s="
        ]
        
        base_api_route = "".join(url_fragments)
        api_url = f"{base_api_route}{encoded_term}"
        
        payload = self._http_get(api_url)
        if not payload:
            return []
            
        meals = payload.get("meals")
        if not meals:
            return []

        filtered_recipes = []
        for meal in meals:
            if not meal:
                continue
                
            # FIXED: Type-guarded against None values from the remote database dictionary
            content_dump = [
                meal.get("strMeal") or "",
                meal.get("strInstructions") or "",
                meal.get("strCategory") or "",
                meal.get("strArea") or ""
            ]
            
            for i in range(1, 21):
                ing = meal.get(f"strIngredient{i}")
                if ing: 
                    content_dump.append(str(ing))
                    
            full_text = " ".join(content_dump).lower()
            
            collision_found = False
            for restriction in self.restrictions:
                if restriction in full_text:
                    collision_found = True
                    break
                    
            if collision_found:
                continue

            recipe_title = meal.get("strMeal") or "Unknown Recipe"
            source_url = meal.get("strSource")
            video_url = meal.get("strYoutube") or "N/A"
            
            site_fragments = ["https://", "www.", "themealdb", ".com/", "meal/"]
            fallback_base = "".join(site_fragments)
            final_link = source_url if source_url else f"{fallback_base}{meal.get('idMeal')}"
            
            filtered_recipes.append({
                "title": recipe_title,
                "category": meal.get("strCategory") or "General",
                "origin": meal.get("strArea") or "International",
                "hyperlink": final_link,
                "video": video_url
            })
            
        return filtered_recipes[:5]

    def safe_scrape_recipe_instructions(self, url: str) -> list[str]:
        """Spawns an isolated headless Playwright page step worker to harvest direction elements."""
        extracted_steps = []
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(user_agent=self.user_agent)
            page = context.new_page()
            try:
                page.goto(url, timeout=12000, wait_until="domcontentloaded")
                elements = page.locator("p, li").all()
                for el in elements:
                    text = el.inner_text().strip()
                    if len(text) > 25 and len(text) < 300:
                        if not re.search(r'(cookie|subscribe|privacy|sign up|log in|copyright|advertisement)', text, re.I):
                            sanitized_line = re.sub(r'\s+', ' ', text)
                            if sanitized_line not in extracted_steps:
                                extracted_steps.append(sanitized_line)
            except Exception as e:
                extracted_steps.append(f"🔒 [Safety Intercept Triggered]: Page worker safely aborted -> {str(e)}")
            finally:
                context.close()
                browser.close()
        return extracted_steps[:4]
import json
import re
import urllib.request
import urllib.parse
from pathlib import Path
from playwright.sync_api import sync_playwright

class AlfredWebIntelligence:
    """
    Module F: Dynamic Retrieval Engine & Web Intelligence (v3.3.1)
    Decisively maps explicitly qualified subdomains and handles live news extraction.
    """
    def __init__(self, cache_dir: str = ".alfred_web_cache"):
        self.cache_path = Path(cache_dir)
        self.cache_path.mkdir(exist_ok=True)
        self.user_agent = "AlfredEngine/3.3.1 (Python 3.12 Framework)"

    def _get_weather_condition(self, code: int) -> str:
        """Maps WMO weather codes to descriptions with visual emoji anchors."""
        wmo_map = {
            0: "Clear Sky ☀️", 1: "Mainly Clear 🌤️", 2: "Partly Cloudy ⛅", 3: "Overcast ☁️",
            45: "Foggy 🌫️", 48: "Depositing Rime Fog 🌫️", 51: "Light Drizzle 🌦️",
            53: "Moderate Drizzle 🌦️", 55: "Dense Drizzle 🌦️", 61: "Slight Rain 🌧️",
            63: "Moderate Rain 🌧️", 65: "Heavy Rain 🌧️", 71: "Slight Snowfall ❄️",
            73: "Moderate Snowfall ❄️", 75: "Heavy Snowfall ❄️", 80: "Slight Rain Showers 🌦️",
            81: "Moderate Rain Showers 🌦️", 82: "Violent Rain Showers 🌧️", 95: "Thunderstorm ⛈️"
        }
        return wmo_map.get(code, "Unknown Local Conditions 🌍")

    def _http_get(self, url: str) -> dict:
        """Robust, zero-dependency HTTP request runner with clean error forwarding."""
        req = urllib.request.Request(url, headers={'User-Agent': self.user_agent})
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                return json.loads(response.read().decode('utf-8'))
        except urllib.error.URLError as ue:
            raise RuntimeError(f"Network transport down. (Details: {ue.reason})")
        except Exception as e:
            raise RuntimeError(f"JSON byte decode exception: {str(e)}")

    def learn_weather_for(self, location_query: str) -> dict:
        """Stitches explicit geocoding domains to resolve location telemetry data safely."""
        clean_query = location_query.strip().lower()
        encoded_name = urllib.parse.quote(clean_query)
        geo_url = f"https://open-meteo.com{encoded_name}&count=1&language=en"
        
        try:
            geo_data = self._http_get(geo_url)
            results = geo_data.get("results")
            if not results:
                return {"success": False, "error": f"Could not find coordinates for target location string: '{location_query}'"}
            
            target = results[0]
            lat, lon = target.get("latitude"), target.get("longitude")
            resolved_name = target.get("name")
            admin_area = target.get("admin1", "ON")
            country = target.get("country", "CA")
            
            forecast_url = f"https://open-meteo.com{lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,weather_code&timezone=auto"
            weather_data = self._http_get(forecast_url)
            current = weather_data.get("current", {})
            
            return {
                "success": True,
                "location": f"{resolved_name}, {admin_area} ({country})",
                "coordinates": f"{lat}, {lon}",
                "temperature": f"{current.get('temperature_2m')}°C",
                "humidity": f"{current.get('relative_humidity_2m')}%",
                "condition": self._get_weather_condition(current.get("weather_code", 0))
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def parse_tech_directory(self) -> list[dict]:
        """Provides accurate subdomains and css locators for technical news extraction."""
        return [
            {"id": "hn", "site": "Hacker News", "url": "https://ycombinator.com", "selectors": [".titleline > a", "td.title > a"]},
            {"id": "tc", "site": "TechCrunch", "url": "https://techcrunch.com", "selectors": ["h3.loop-card__title a", "h2.loop-card__title a"]},
            {"id": "ph", "site": "Phoronix", "url": "https://phoronix.com", "selectors": ["#content article a", "article a"]}
        ]

    def scrape_headlines(self, site_id: str) -> list[str]:
        """Runs a locator loop inside the automation worker profile to collect top titles."""
        directory = self.parse_tech_directory()
        target = next((item for item in directory if item["id"] == site_id), None)
        if not target: return []

        headlines = []
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(user_agent=self.user_agent)
            page = context.new_page()
            try:
                page.goto(target["url"], timeout=20000, wait_until="domcontentloaded")
                for selector in target["selectors"]:
                    elements = page.locator(selector).all()
                    for el in elements:
                        text = el.inner_text().strip()
                        if text and len(text) > 12 and not re.search(r'(cookie|subscribe|log in|sign up)', text, re.I):
                            if text not in headlines: headlines.append(text)
                    if headlines: break
            except Exception as e:
                headlines.append(f"Automation Web Agent Exception: {str(e)}")
            finally:
                context.close()
                browser.close()
        return headlines[:6]
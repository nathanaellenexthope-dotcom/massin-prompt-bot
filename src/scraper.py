#!/usr/bin/env python3
import os
import re
import requests
from bs4 import BeautifulSoup
from thefuzz import fuzz


class MassInScraper:
    def __init__(self):
        self.sites = [
            "https://www.mass-in.com",
            "https://www.music.mass-in.com"
        ]
        
    def search_product(self, product_name: str) -> dict | None:
        """Recherche un produit par nom sur les deux sites."""
        print(f"Recherche: {product_name}")
        
        all_candidates = []
        for site in self.sites:
            candidates = self._scrape_site(site, product_name)
            all_candidates.extend(candidates)
        
        best = self._find_best_match(product_name, all_candidates)
        
        if not best:
            print(f"Aucun produit correspondant trouve pour '{product_name}'")
            return None
        
        image_data = self._extract_product_image(best.get("soup"), best.get("name"))
        
        return {
            "name": best["name"],
            "url": best.get("url", ""),
            "image_url": image_data["url"] if image_data else "",
            "source": best.get("source", "")
        }
    
    def _scrape_site(self, base_url: str, product_name: str) -> list[dict]:
        """Scrape la page de recherche."""
        try:
            search_url = f"{base_url}/search?q={requests.utils.quote(product_name)}"
            resp = requests.get(search_url, timeout=15, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            })
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            products = []
            for item in soup.select('.product-item, .product, [class*="product"]'):
                name_elem = item.select_one('.product-name, .product-title, h2, h3')
                if name_elem:
                    products.append({
                        "name": name_elem.get_text(strip=True),
                        "url": item.find('a', href=True)['href'] if item.find('a', href=True) else "",
                        "soup": item,
                        "source": base_url
                    })
            return products
            
        except Exception as e:
            print(f"[ERREUR SCRAPE {base_url}] {e}")
            return []

    def _find_best_match(self, query: str, candidates: list[dict]) -> dict | None:
        """Trouve le meilleur match avec un score minimum requis."""
        if not candidates:
            return None
        
        best_match = None
        best_score = 0.0
        query_lower = query.lower().strip()
        query_words = set(query_lower.split())
        
        for candidate in candidates:
            name = candidate.get("name", "").lower().strip()
            
            fuzz_ratio = fuzz.ratio(query_lower, name) / 100.0
            name_words = set(name.split())
            common_words = len(query_words & name_words) / max(len(query_words), len(name_words), 1)
            
            score = (fuzz_ratio * 0.7) + (common_words * 0.3)
            
            if query_lower in name:
                score += 0.15
            
            if score > best_score:
                best_score = score
                best_match = candidate
        
        MIN_SCORE = 0.65
        if best_score < MIN_SCORE:
            print(f"[MATCH REJETE] Score {best_score:.2f} < {MIN_SCORE} pour '{query}'")
            return None
        
        print(f"[MATCH TROUVE] '{best_match['name']}' (score: {best_score:.2f})")
        return best_match
    
    def _extract_product_image(self, soup, product_name: str) -> dict | None:
        """Extrait l'image produit en filtrant les logos. Fallback Unsplash."""
        if not soup:
            return self._get_unsplash_image(product_name)
        
        LOGO_PATTERNS = [
            r'logo', r'icon', r'favicon', r'header', r'banner',
            r'nav', r'footer', r'logo-mass', r'mass-in-logo',
            r'\.svg$', r'user-', r'cart-', r'menu-', r'arrow-'
        ]
        
        images = soup.find_all('img')
        valid_images = []
        
        for img in images:
            src = img.get('src', '') or img.get('data-src', '')
            alt = img.get('alt', '').lower()
            
            if not src:
                continue
            
            is_logo = any(re.search(pattern, src, re.I) or re.search(pattern, alt, re.I) 
                           for pattern in LOGO_PATTERNS)
            
            if is_logo:
                continue
            
            width = img.get('width', '')
            height = img.get('height', '')
            if width and height:
                try:
                    w, h = int(width), int(height)
                    if w < 100 or h < 100:
                        continue
                except ValueError:
                    pass
            
            if src.startswith('/'):
                base = "https://www.mass-in.com"
                src = f"{base}{src}"
            elif not src.startswith('http'):
                continue
            
            valid_images.append({
                "url": src,
                "alt": alt,
                "source": "site"
            })
        
        if not valid_images:
            unsplash = self._get_unsplash_image(product_name)
            if unsplash:
                return {"url": unsplash, "alt": product_name, "source": "unsplash"}
        
        return valid_images[0] if valid_images else None
    
    def _get_unsplash_image(self, query: str) -> str | None:
        """Recherche une image sur Unsplash API."""
        access_key = os.getenv("UNSPLASH_ACCESS_KEY")
        if not access_key:
            return None
        
        url = "https://api.unsplash.com/search/photos"
        headers = {"Authorization": f"Client-ID {access_key}"}
        params = {"query": query, "per_page": 1, "orientation": "squarish"}
        
        try:
            resp = requests.get(url, headers=headers, params=params, timeout=10)
            data = resp.json()
            results = data.get("results", [])
            if results:
                return results[0]["urls"]["regular"]
        except Exception as e:
            print(f"[UNSPLASH ERROR] {e}")
        
        return None

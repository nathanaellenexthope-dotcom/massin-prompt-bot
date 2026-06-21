import requests
from bs4 import BeautifulSoup
import urllib.parse
from urllib.parse import urlparse

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

class ProductScraper:
    def __init__(self):
        self.sites = [
            'https://www.mass-in.com',
            'https://www.music.mass-in.com'
        ]
    
    def search_product(self, product_name):
        results = []
        for site in self.sites:
            try:
                product_info = self._find_product_on_site(site, product_name)
                if product_info:
                    results.append(product_info)
            except Exception as e:
                print(f"  [ERREUR] Sur {site}: {e}")
                continue
        
        if results:
            return max(results, key=lambda x: len(x.get('description', '')))
        return None
    
    def _find_product_on_site(self, base_url, product_name):
        search_url = f"{base_url}/shop/search?search={urllib.parse.quote(product_name)}"
        
        try:
            print(f"  [INFO] Recherche sur {base_url}...")
            response = requests.get(search_url, headers=HEADERS, timeout=15)
            print(f"  [INFO] Status code: {response.status_code}")
            soup = BeautifulSoup(response.content, 'html.parser')
            product_links = self._extract_product_links(soup, base_url)
            print(f"  [INFO] {len(product_links)} liens de produits trouves")
            
            if product_links:
                best_link = self._find_best_match(product_links, product_name)
                if best_link:
                    print(f"  [INFO] Meilleur match: {best_link}")
                    return self._scrape_product_page(best_link)
        except Exception as e:
            print(f"  [ERREUR] Recherche sur {base_url}: {e}")
        
        try:
            print(f"  [INFO] Tentative sur page d accueil {base_url}...")
            response = requests.get(base_url, headers=HEADERS, timeout=15)
            soup = BeautifulSoup(response.content, 'html.parser')
            product_links = self._extract_product_links(soup, base_url)
            best_link = self._find_best_match(product_links, product_name)
            if best_link:
                return self._scrape_product_page(best_link)
        except Exception as e:
            print(f"  [ERREUR] Page d accueil {base_url}: {e}")
        
        return None
    
    def _extract_product_links(self, soup, base_url):
        links = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            if any(pattern in href.lower() for pattern in ['/product/', '/shop/', '/produit/', '/item/']):
                full_url = href if href.startswith('http') else base_url + href
                links.append({'url': full_url, 'text': a.get_text(strip=True)})
        return links
    
    def _find_best_match(self, links, product_name):
        if not links:
            return None
        product_words = set(product_name.lower().split())
        best_score = 0
        best_link = None
        for link in links:
            link_text = link['text'].lower()
            score = sum(1 for word in product_words if word in link_text)
            if score > best_score:
                best_score = score
                best_link = link['url']
        return best_link
    
    def _scrape_product_page(self, product_url):
        try:
            print(f"  [INFO] Scraping page: {product_url}")
            response = requests.get(product_url, headers=HEADERS, timeout=15)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            name = self._extract_product_name(soup)
            image_url = self._extract_product_image(soup, product_url)
            description = self._extract_description(soup)
            category = self._detect_category(name, description)
            
            return {
                'name': name or 'Produit inconnu',
                'image_url': image_url or '',
                'product_url': product_url,
                'description': description or '',
                'category': category,
                'source': product_url
            }
        except Exception as e:
            print(f"  [ERREUR] Scraping page {product_url}: {e}")
            return None
    
    def _extract_product_name(self, soup):
        selectors = [
            'h1.product-title', 'h1.product_name', 'h1.entry-title',
            '.product-title h1', 'h1[itemprop="name"]', 'h1'
        ]
        for selector in selectors:
            elem = soup.select_one(selector)
            if elem:
                return elem.get_text(strip=True)
        return None
    
    def _extract_product_image(self, soup, base_url):
        selectors = [
            'img.wp-post-image', 'img.attachment-woocommerce_single',
            'img[itemprop="image"]', '.woocommerce-product-gallery__image img',
            '.product-image img', 'figure img'
        ]
        for selector in selectors:
            img = soup.select_one(selector)
            if img:
                src = img.get('data-src') or img.get('src')
                if src:
                    if src.startswith('//'):
                        src = 'https:' + src
                    elif src.startswith('/'):
                        parsed = urlparse(base_url)
                        src = f"{parsed.scheme}://{parsed.netloc}{src}"
                    return src
        return None
    
    def _extract_description(self, soup):
        selectors = [
            '.product-description', '.woocommerce-product-details__short-description',
            '[itemprop="description"]', '.description', '.product-summary'
        ]
        for selector in selectors:
            elem = soup.select_one(selector)
            if elem:
                return elem.get_text(strip=True)
        return None
    
    def _detect_category(self, name, description):
        text = f"{name} {description}".lower()
        categories = {
            'smartphone': ['smartphone', 'phone', 'mobile', 'redmagic', 'iphone', 'samsung'],
            'casque': ['casque', 'headphone', 'headset', 'ecouteur', 'earphone', 'hdj'],
            'enceinte': ['enceinte', 'speaker', 'boombox', 'partybox', 'soundbar'],
            'console': ['console', 'ps5', 'playstation', 'xbox', 'nintendo', 'switch'],
            'laptop': ['laptop', 'ordinateur', 'pc', 'notebook', 'thinkpad', 'hp', 'lenovo'],
            'platine': ['platine', 'dj', 'mixstream', 'pioneer', 'numark', 'controller'],
            'accessoire': ['accessoire', 'cable', 'housse', 'chargeur', 'adaptateur']
        }
        for cat, keywords in categories.items():
            if any(kw in text for kw in keywords):
                return cat
        return 'produit'

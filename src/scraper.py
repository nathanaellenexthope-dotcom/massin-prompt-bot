import requests
from bs4 import BeautifulSoup
import urllib.parse
from urllib.parse import urlparse

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
}

class ProductScraper:
    def __init__(self):
        self.sites = [
            'https://www.mass-in.com',
            'https://www.music.mass-in.com'
        ]
    
    def search_product(self, product_name):
        """Recherche un produit sur les deux sites."""
        print(f"[INFO] Recherche du produit: '{product_name}'")
        
        for site in self.sites:
            try:
                print(f"[INFO] Tentative sur {site}...")
                product_info = self._search_on_site(site, product_name)
                if product_info:
                    print(f"[SUCCES] Produit trouve sur {site}")
                    return product_info
            except Exception as e:
                print(f"[ERREUR] Sur {site}: {e}")
                continue
        
        print(f"[ECHEC] Produit '{product_name}' non trouve sur les sites")
        return None
    
    def _search_on_site(self, base_url, product_name):
        """Recherche un produit sur un site specifique."""
        
        # Essayer differentes URL de recherche (structure Shopify/WooCommerce)
        search_urls = [
            f"{base_url}/shop/?s={urllib.parse.quote(product_name)}",
            f"{base_url}/?s={urllib.parse.quote(product_name)}",
            f"{base_url}/shop/search?search={urllib.parse.quote(product_name)}",
            f"{base_url}/recherche?search={urllib.parse.quote(product_name)}",
            f"{base_url}/produit/?s={urllib.parse.quote(product_name)}",
            f"{base_url}/products/?s={urllib.parse.quote(product_name)}",
        ]
        
        for search_url in search_urls:
            try:
                print(f"  [INFO] URL de recherche: {search_url}")
                response = requests.get(search_url, headers=HEADERS, timeout=15, allow_redirects=True)
                print(f"  [INFO] Status: {response.status_code}")
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Chercher tous les liens de produits
                    product_links = self._extract_all_product_links(soup, base_url)
                    print(f"  [INFO] {len(product_links)} liens trouves")
                    
                    if product_links:
                        # Trouver le meilleur match
                        best_match = self._find_best_match(product_links, product_name)
                        if best_match:
                            print(f"  [INFO] Meilleur match: {best_match['text'][:50]}")
                            return self._scrape_product_page(best_match['url'])
            except Exception as e:
                print(f"  [ERREUR] URL {search_url}: {e}")
                continue
        
        # Si la recherche echoue, essayer la page d'accueil
        try:
            print(f"  [INFO] Tentative sur page d'accueil...")
            response = requests.get(base_url, headers=HEADERS, timeout=15)
            soup = BeautifulSoup(response.content, 'html.parser')
            product_links = self._extract_all_product_links(soup, base_url)
            
            if product_links:
                best_match = self._find_best_match(product_links, product_name)
                if best_match:
                    return self._scrape_product_page(best_match['url'])
        except Exception as e:
            print(f"  [ERREUR] Page d'accueil: {e}")
        
        return None
    
    def _extract_all_product_links(self, soup, base_url):
        """Extrait tous les liens de produits possibles."""
        links = []
        
        for a in soup.find_all('a', href=True):
            href = a['href']
            text = a.get_text(strip=True)
            
            is_product = False
            
            # Patterns d'URL specifiques aux sites mass-in
            url_patterns = [
                '/product/', '/produit/', '/shop/', '/item/',
                '/p/', '/products/', '/boutique/', '/catalogue/'
            ]
            
            for pattern in url_patterns:
                if pattern in href.lower():
                    is_product = True
                    break
            
            if text and len(text) > 3 and not text.lower() in ['home', 'accueil', 'shop', 'boutique', 'cart', 'panier']:
                if not is_product and href.startswith(base_url):
                    is_product = True
            
            if is_product and href and text:
                full_url = href if href.startswith('http') else base_url + href
                links.append({'url': full_url, 'text': text})
        
        return links
    
    def _find_best_match(self, links, product_name):
        """Trouve le lien le plus pertinent."""
        if not links:
            return None
        
        product_words = set(product_name.lower().split())
        best_score = -1
        best_link = None
        
        for link in links:
            link_text = link['text'].lower()
            url_text = link['url'].lower()
            
            # Score base sur le texte
            text_score = sum(2 for word in product_words if word in link_text)
            # Score base sur l'URL
            url_score = sum

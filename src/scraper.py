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
        """Recherche un produit sur les sites mass-in, sinon cherche une image sur internet."""
        print(f"[INFO] Recherche du produit: '{product_name}'")
        
        # 1. Essayer de trouver sur mass-in.com et music.mass-in.com
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
        
        # 2. Si non trouve, chercher une image sur internet
        print(f"[INFO] Produit non trouve sur les sites. Recherche d'image sur internet...")
        image_url = self._search_image_google(product_name)
        
        # 3. Retourner les infos avec le nom fourni et l'image trouvee
        result = {
            'name': product_name,
            'image_url': image_url or '',
            'product_url': '',
            'description': '',
            'category': self._detect_category(product_name, ''),
            'source': 'internet' if image_url else 'non_trouve'
        }
        
        if image_url:
            print(f"[SUCCES] Image trouvee sur internet: {image_url[:80]}...")
        else:
            print(f"[ATTENTION] Aucune image trouvee pour '{product_name}'")
        
        return result
    
    def _search_on_site(self, base_url, product_name):
        """Recherche un produit sur un site specifique."""
        
        # Essayer differentes URL de recherche
        search_urls = [
            f"{base_url}/shop/?s={urllib.parse.quote(product_name)}",
            f"{base_url}/?s={urllib.parse.quote(product_name)}",
            f"{base_url}/shop/search?search={urllib.parse.quote(product_name)}",
            f"{base_url}/recherche?search={urllib.parse.quote(product_name)}",
            f"{base_url}/produit/?s={urllib.parse.quote(product_name)}",
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
        
        return None
    
    def _search_image_google(self, product_name):
        """Cherche une image du produit sur internet via DuckDuckGo (plus simple que Google)."""
        try:
            # Utiliser DuckDuckGo Image Search (API simple, pas de blocage)
            search_query = urllib.parse.quote(product_name + " product")
            url = f"https://duckduckgo.com/?q={search_query}&iax=images&ia=images"
            
            response = requests.get(url, headers=HEADERS, timeout=10)
            
            # Extraire les URLs d'images du HTML
            # Chercher les patterns d'images dans le HTML
            import re
            image_urls = re.findall(r'https?://[^"\s]+\.(?:jpg|jpeg|png|webp)', response.text)
            
            # Filtrer les URLs valides
            for img_url in image_urls:
                if 'icon' not in img_url.lower() and 'logo' not in img_url.lower():
                    if len(img_url) > 20:
                        return img_url
            
            # Fallback: utiliser une URL d'image generique
            return self._get_generic_image(product_name)
            
        except Exception as e:
            print(f"  [ERREUR] Recherche image: {e}")
            return self._get_generic_image(product_name)
    
    def _get_generic_image(self, product_name):
        """Retourne une URL d'image generique basee sur la categorie."""
        category = self._detect_category(product_name, '')
        
        # URLs d'images generiques par categorie
        generic_images = {
            'smartphone': 'https://via.placeholder.com/400x600/4CAF50/FFFFFF?text=Smartphone',
            'casque': 'https://via.placeholder.com/400x600/2196F3/FFFFFF?text=Casque',
            'enceinte': 'https://via.placeholder.com/400x600/FF9800/FFFFFF?text=Enceinte',
            'console': 'https://via.placeholder.com/400x600/F44336/FFFFFF?text=Console',
            'laptop': 'https://via.placeholder.com/400x600/9C27B0/FFFFFF?text=Laptop',
            'platine': 'https://via.placeholder.com/400x600/00BCD4/FFFFFF?text=Platine+DJ',
            'tablette': 'https://via.placeholder.com/400x600/3F51B5/FFFFFF?text=Tablette',
            'montre': 'https://via.placeholder.com/400x600/E91E63/FFFFFF?text=Montre',
            'accessoire': 'https://via.placeholder.com/400x600/607D8B/FFFFFF?text=Accessoire',
            'produit': 'https://via.placeholder.com/400x600/795548/FFFFFF?text=Produit'
        }
        
        return generic_images.get(category, generic_images['produit'])
    
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
            url_score = sum(1 for word in product_words if word in url_text)
            # Bonus si le nom exact est dans le texte
            exact_bonus = 5 if product_name.lower() in link_text else 0
            
            total_score = text_score + url_score + exact_bonus
            
            if total_score > best_score:
                best_score = total_score
                best_link = link
        
        # Ne retourner que si le score est suffisant
        if best_score >= 2:
            return best_link
        return None
    
    def _scrape_product_page(self, product_url):
        """Scrape une page produit pour extraire les informations."""
        try:
            print(f"  [INFO] Scraping: {product_url}")
            response = requests.get(product_url, headers=HEADERS, timeout=15)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            name = self._extract_product_name(soup)
            image_url = self._extract_product_image(soup, product_url)
            description = self._extract_description(soup)
            category = self._detect_category(name, description)
            
            result = {
                'name': name or 'Produit inconnu',
                'image_url': image_url or '',
                'product_url': product_url,
                'description': description or '',
                'category': category,
                'source': product_url
            }
            
            print(f"  [INFO] Nom: {result['name'][:50]}")
            print(f"  [INFO] Image: {result['image_url'][:80] if result['image_url'] else 'AUCUNE'}")
            print(f"  [INFO] Categorie: {category}")
            
            return result
            
        except Exception as e:
            print(f"  [ERREUR] Scraping page {product_url}: {e}")
            return None
    
    def _extract_product_name(self, soup):
        """Extrait le nom du produit."""
        selectors = [
            'h1.product-title', 'h1.product_name', 'h1.entry-title',
            '.product-title h1', 'h1[itemprop="name"]',
            '.woocommerce-product-details__short-description h2',
            'h1',
        ]
        for selector in selectors:
            elem = soup.select_one(selector)
            if elem:
                name = elem.get_text(strip=True)
                if name and len(name) > 2:
                    return name
        return None
    
    def _extract_product_image(self, soup, base_url):
        """Extrait l'URL de l'image du produit."""
        selectors = [
            'img.wp-post-image',
            'img.attachment-woocommerce_single',
            'img.attachment-woocommerce_thumbnail',
            'img[itemprop="image"]',
            '.woocommerce-product-gallery__image img',
            '.woocommerce-product-gallery__image--placeholder img',
            '.product-image img',
            'figure img',
            '.wp-block-image img',
            'img[data-src]',
        ]
        
        for selector in selectors:
            img = soup.select_one(selector)
            if img:
                src = img.get('data-src') or img.get('data-lazy-src') or img.get('src')
                if src:
                    if src.startswith('//'):
                        src = 'https:' + src
                    elif src.startswith('/'):
                        parsed = urlparse(base_url)
                        src = f"{parsed.scheme}://{parsed.netloc}{src}"
                    
                    if any(ext in src.lower() for ext in ['.jpg', '.jpeg', '.png', '.webp', '.gif']):
                        return src
                    elif 'wp-content' in src or 'uploads' in src:
                        return src
        
        # Chercher toutes les images de la page
        all_images = soup.find_all('img')
        for img in all_images:
            src = img.get('data-src') or img.get('data-lazy-src') or img.get('src')
            if src and len(src) > 10:
                if src.startswith('//'):
                    src = 'https:' + src
                elif src.startswith('/'):
                    parsed = urlparse(base_url)
                    src = f"{parsed.scheme}://{parsed.netloc}{src}"
                
                width = img.get('width', '')
                if width and width.isdigit() and int(width) < 100:
                    continue
                
                if any(ext in src.lower() for ext in ['.jpg', '.jpeg', '.png', '.webp']):
                    return src
        
        return None
    
    def _extract_description(self, soup):
        """Extrait la description du produit."""
        selectors = [
            '.product-description',
            '.woocommerce-product-details__short-description',
            '[itemprop="description"]',
            '.description',
            '.product-summary',
            '.woocommerce-product-details',
        ]
        for selector in selectors:
            elem = soup.select_one(selector)
            if elem:
                desc = elem.get_text(strip=True)
                if desc and len(desc) > 10:
                    return desc
        return None
    
    def _detect_category(self, name, description):
        """Detecte la categorie du produit pour adapter le prompt."""
        text = f"{name} {description}".lower() if name else ""
        
        categories = {
            'smartphone': ['smartphone', 'phone', 'mobile', 'redmagic', 'iphone', 'samsung', 'xiaomi', 'oppo'],
            'casque': ['casque', 'headphone', 'headset', 'ecouteur', 'earphone', 'hdj', 'airpods', 'beats'],
            'enceinte': ['enceinte', 'speaker', 'boombox', 'partybox', 'soundbar', 'jbl', 'bose', 'sonos'],
            'console': ['console', 'ps5', 'playstation', 'xbox', 'nintendo', 'switch'],
            'laptop': ['laptop', 'ordinateur', 'pc', 'notebook', 'thinkpad', 'hp', 'lenovo', 'macbook'],
            'platine': ['platine', 'dj', 'mixstream', 'pioneer', 'numark', 'controller', 'deck'],
            'tablette': ['tablette', 'tablet', 'ipad', 'galaxy tab'],
            'montre': ['montre', 'watch', 'smartwatch', 'apple watch', 'galaxy watch'],
            'accessoire': ['accessoire', 'cable', 'housse', 'chargeur', 'adaptateur', 'etui', 'support']
        }
        
        for cat, keywords in categories.items():
            if any(kw in text for kw in keywords):
                return cat
        return 'produit'

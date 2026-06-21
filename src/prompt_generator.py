import random

class PromptGenerator:
    COLORS = [
        'vert clair', 'jaune', 'rouge', 'bleu dynamique', 'orange',
        'violet', 'rose', 'bleu marine', 'gris clair', 'turquoise'
    ]
    
    MODEL_TYPES = [
        'une jeune femme malagasy agee de 18 a 25 ans',
        "une personne d'origine malgache",
        'une femme malgache nerdy girl beautiful with glasses',
        'un jeune homme malgache age de 20 a 30 ans',
        "une personne d'origine malgache, style moderne et tendance"
    ]
    
    def generate_prompt(self, product_info):
        category = product_info.get('category', 'produit')
        name = product_info.get('name', 'Produit')
        color = random.choice(self.COLORS)
        model = random.choice(self.MODEL_TYPES)
        
        if category == 'smartphone':
            return self._generate_smartphone_prompt(name, color, model)
        elif category == 'casque':
            return self._generate_headphone_prompt(name, color, model)
        elif category == 'enceinte':
            return self._generate_speaker_prompt(name, color, model)
        elif category == 'console':
            return self._generate_console_prompt(name, color, model)
        elif category == 'laptop':
            return self._generate_laptop_prompt(name, color, model)
        elif category == 'platine':
            return self._generate_dj_prompt(name, color, model)
        else:
            return self._generate_generic_prompt(name, color, model, category)
    
    def _generate_smartphone_prompt(self, name, color, model):
        return f"Je suis sur un visuel qui met en valeur un smartphone, voici les details du produit ({name}). Je veux un visuel neutre de produit, sans texte, avec un angle dynamique en vue de bas, l'angle du smartphone etant ajuste. {model} tient le smartphone avec des gestes dynamiques (gestes aleatoires), et le visuel est zoome sur l'objet principal tout en permettant de bien voir la personne. Le fond est en studio de couleur {color} et le format du visuel est 9:16."
    
    def _generate_headphone_prompt(self, name, color, model):
        return f"Je suis sur un visuel qui met en valeur ce produit. Voici les details du produit : ({name}). Je veux un visuel publicitaire premium, sans texte ni logo ajoute. Le produit doit etre l'element principal de la composition, avec un angle dynamique en contre-plongee (vue de bas) afin de renforcer son impact visuel. Ajuste l'angle et la perspective pour maximiser sa presence a l'ecran. {model} porte le produit (casque) sur sa tete de maniere naturelle et authentique. Elle doit etre clairement visible dans le cadrage, avec un visage harmonieux, une apparence moderne et soignee, et une expression confiante accompagnee d'un leger sourire naturel. Sa posture doit etre dynamique et engageante, avec des gestes spontanes et naturels (random natural gestures) qui transmettent de l'energie, de la confiance et un style de vie actif. Effectue un zoom sur le produit afin qu'il reste le point focal de l'image, tout en conservant une excellente visibilite du visage, du casque et du haut du corps du modele. La composition doit equilibrer parfaitement la mise en avant du produit et la presence humaine. Le fond doit etre un studio propre et minimaliste de couleur {color}, avec un eclairage professionnel de type photographie publicitaire premium. Mets en valeur les details, les textures et les finitions du produit grace a une lumiere douce et maitrisee. Style photorealiste ultra-realiste, photographie commerciale haut de gamme, qualite e-commerce premium, haute definition, nettete exceptionnelle, profondeur de champ subtile, ombres douces et rendu naturel. Toutes les personnes presentes dans l'image doivent etre d'origine malagasy. Format vertical 9:16."
    
    def _generate_speaker_prompt(self, name, color, model):
        return f"Je suis en train de creer un visuel publicitaire mettant en valeur ce produit. Voici les details du produit : ({name}). Genere une photo publicitaire professionnelle et realiste, sans aucun texte ni logo ajoute sur l'image. L'objet principal est une enceinte, qui doit etre clairement visible et occuper une place dominante dans la composition. Utilise un angle de prise de vue dynamique en contre-plongee (vue de bas vers le haut) afin de renforcer la presence et l'impact visuel du produit. Ajuste l'orientation de l'enceinte pour mettre en avant son design, ses details et son volume. Integre {model} tenant l'enceinte avec des gestes naturels et dynamiques (pose spontanee, mouvement de presentation, manipulation du produit ou interaction authentique avec celui-ci). La personne doit etre entierement visible ou majoritairement visible dans le cadre, avec une expression naturelle et engageante. Effectue un zoom modere sur la scene afin que l'enceinte reste l'element principal tout en conservant une bonne visibilite de la personne. La composition doit etre equilibree entre le produit et le modele. Toutes les personnes presentes sur l'image doivent etre d'origine malgache et representees de maniere realiste. Utilise un fond studio uni de couleur ({color}), propre, moderne et professionnel, avec un eclairage publicitaire de haute qualite mettant en valeur les volumes, les textures et les materiaux de l'enceinte. Style : photographie publicitaire premium, rendu photorealiste, details nets, profondeur de champ maitrisee, eclairage studio professionnel, qualite e-commerce haut de gamme. Format vertical 9:16. Aucun texte, aucun slogan, aucun element graphique superpose."
    
    def _generate_console_prompt(self, name, color, model):
        return f"Je suis sur un visuel qui met en valeur ce produit, voici les details du produit ({name}). Je veux un visuel produit neutre, sans aucun texte ni logo. Utilise un angle dynamique en contre-plongee (vue de bas) pour donner de l'impact visuel. Ajuste l'orientation du produit afin qu'il soit parfaitement visible et mis en avant. Fais en sorte que {model} soit clairement visible dans l'image, tenant la console avec ses deux mains dans une pose dynamique et naturelle, comme lors d'une demonstration ou presentation du produit. La personne porte egalement une montre avec motif ou design inspire d'une souris, bien visible au poignet. Mets l'accent sur le produit principal avec un leger zoom, tout en conservant suffisamment de cadrage pour voir clairement la personne. Utilise des gestes expressifs et dynamiques pour renforcer l'aspect publicitaire. Le fond doit etre un studio professionnel de couleur ({color}), propre, uniforme et minimaliste. Style photographie publicitaire haut de gamme, eclairage studio maitrise, details nets, rendu realiste, qualite premium. Format vertical 9:16."
    
    def _generate_laptop_prompt(self, name, color, model):
        return f"Je suis en train de creer un visuel publicitaire mettant en valeur ce produit. Voici les details du produit : ({name}). Genere une photo publicitaire professionnelle et realiste, sans aucun texte ni logo ajoute sur l'image. L'objet principal est un laptop, qui doit etre clairement visible et occuper une place dominante dans la composition. Utilise un angle de prise de vue dynamique en contre-plongee (vue de bas vers le haut) afin de renforcer la presence et l'impact visuel du produit. Ajuste l'orientation du laptop pour mettre en avant son design, son ecran et son clavier. Integre {model} utilisant le laptop avec des gestes naturels et dynamiques (pose spontanee, mouvement de presentation, interaction authentique avec celui-ci). La personne doit etre entierement visible ou majoritairement visible dans le cadre, avec une expression naturelle et engageante. Effectue un zoom modere sur la scene afin que le laptop reste l'element principal tout en conservant une bonne visibilite de la personne. La composition doit etre equilibree entre le produit et le modele. Toutes les personnes presentes sur l'image doivent etre d'origine malgache et representees de maniere realiste. Utilise un fond studio uni de couleur ({color}), propre, moderne et professionnel, avec un eclairage publicitaire de haute qualite mettant en valeur les volumes, les textures et les materiaux du laptop. Style : photographie publicitaire premium, rendu photorealiste, details nets, profondeur de champ maitrisee, eclairage studio professionnel, qualite e-commerce haut de gamme. Format vertical 9:16. Aucun texte, aucun slogan, aucun element graphique superpose."
    
    def _generate_dj_prompt(self, name, color, model):
        return f"Je suis sur un visuel qui met en valeur ce produit, voici les details du produit ({name}). Je veux un visuel produit neutre, sans aucun texte ni logo. Utilise un angle dynamique en contre-plongee (vue de bas) pour donner de l'impact visuel. Ajuste l'orientation du produit afin qu'il soit parfaitement visible et mis en avant. Fais en sorte que {model} soit clairement visible dans l'image, manipulant la platine DJ avec ses deux mains dans une pose dynamique et naturelle, comme lors d'une performance ou demonstration du produit. La personne porte egalement une montre avec motif ou design inspire d'une souris, bien visible au poignet. Mets l'accent sur le produit principal avec un leger zoom, tout en conservant suffisamment de cadrage pour voir clairement la personne. Utilise des gestes expressifs et dynamiques pour renforcer l'aspect publicitaire. Le fond doit etre un studio professionnel de couleur ({color}), propre, uniforme et minimaliste. Style photographie publicitaire haut de gamme, eclairage studio maitrise, details nets, rendu realiste, qualite premium. Format vertical 9:16."
    
    def _generate_generic_prompt(self, name, color, model, category):
        return f"Je suis en train de creer un visuel publicitaire mettant en valeur ce produit. Voici les details du produit : ({name}). Genere une photo publicitaire professionnelle et realiste, sans aucun texte ni logo ajoute sur l'image. L'objet principal est un {category}, qui doit etre clairement visible et occuper une place dominante dans la composition. Utilise un angle de prise de vue dynamique en contre-plongee (vue de bas vers le haut) afin de renforcer la presence et l'impact visuel du produit. Integre {model} tenant ou utilisant le {category} avec des gestes naturels et dynamiques (pose spontanee, mouvement de presentation, manipulation du produit ou interaction authentique avec celui-ci). La personne doit etre entierement visible ou majoritairement visible dans le cadre, avec une expression naturelle et engageante. Effectue un zoom modere sur la scene afin que le {category} reste l'element principal tout en conservant une bonne visibilite de la personne. La composition doit etre equilibree entre le produit et le modele. Toutes les personnes presentes sur l'image doivent etre d'origine malgache et representees de maniere realiste. Utilise un fond studio uni de couleur ({color}), propre, moderne et professionnel, avec un eclairage publicitaire de haute qualite mettant en valeur les volumes, les textures et les materiaux du {category}. Style : photographie publicitaire premium, rendu photorealiste, details nets, profondeur de champ maitrisee, eclairage studio professionnel, qualite e-commerce haut de gamme. Format vertical 9:16. Aucun texte, aucun slogan, aucun element graphique superpose."

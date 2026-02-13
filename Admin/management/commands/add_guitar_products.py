"""
Management command to add guitar product images from the images/ folder
into the Guitars category with random prices between 15,000 and 30,000.
"""
import random
from pathlib import Path

from django.core.files import File
from django.core.management.base import BaseCommand
from django.conf import settings

from Admin.category.models import categoryModel
from Admin.subcategory.models import brandModel
from Admin.product.models import productModel


# 8 guitar images and their product names (from project images/ folder)
GUITAR_PRODUCTS = [
    ("alejandro-morelos-6WOtQjsxlpU-unsplash.jpg", "Epiphone Explorer Electric Guitar"),
    ("black-white-electric-guitar.png", "Black Stratocaster Electric Guitar"),
    ("OIUGBN0.jpg", "Blue Electric Guitar"),
    ("3d-music-related-scene.jpg", "Orange-Red Stratocaster Electric Guitar"),
    ("274.jpg", "Stratocaster Triple Pack (Black, Red, Blue)"),
    ("martin-rajdl-Olg60_RTPc8-unsplash.jpg", "Fender Stratocaster White"),
    ("apolo-photographer-xmksM4em7a0-unsplash.jpg", "Sunburst Semi-Hollow Electric Guitar"),
    ("electric-guitar-with-neon-light-still-life.jpg", "Fender Stratocaster White Neon"),
]


class Command(BaseCommand):
    help = "Add guitar images from images/ folder as products in Guitars category with random prices 15000-30000"

    def handle(self, *args, **options):
        base_dir = Path(settings.BASE_DIR)
        images_dir = base_dir / "images"
        if not images_dir.exists():
            self.stderr.write(self.style.ERROR(f"Images directory not found: {images_dir}"))
            return

        # Get or create Guitars category
        guitar_cat = categoryModel.objects.filter(cat_name__icontains="guitar").first()
        if not guitar_cat:
            guitar_cat = categoryModel.objects.first()
        if not guitar_cat:
            guitar_cat = categoryModel.objects.create(cat_name="Guitars")
            self.stdout.write(self.style.SUCCESS("Created category 'Guitars'."))

        # Get or create a brand for guitars
        brand, _ = brandModel.objects.get_or_create(
            brand_name="Sachris Club",
            defaults={"brand_name": "Sachris Club"},
        )

        created = 0
        for idx, (filename, product_name) in enumerate(GUITAR_PRODUCTS, start=1):
            src = images_dir / filename
            if not src.exists():
                self.stdout.write(self.style.WARNING(f"Skip (file not found): {filename}"))
                continue

            # Random price between 15000 and 30000
            price = random.randint(15000, 30000)
            strike_price = price + random.randint(1000, 5000)  # optional higher strike price

            # Unique main image name under ProductImage/Main (safe for filesystem)
            ext = src.suffix
            safe_name = f"guitar_{idx}{ext}"

            pro = productModel(
                catname_id=guitar_cat,
                brand=brand,
                productname=product_name,
                pro_description=f"Electric guitar - {product_name}. Quality instrument for beginners and professionals.",
                pro_code=random.randint(10000, 99999),
                total_quantity=10,
                pro_price=price,
                strike_price=strike_price,
                pro_colour="Various",
                return_product="Yes",
                return_period_days=7,
                pro_height=100,
                pro_width=40,
                pro_length=10,
            )
            pro.save()

            with open(src, "rb") as f:
                pro.pro_image.save(safe_name, File(f), save=True)

            created += 1
            self.stdout.write(
                self.style.SUCCESS(f"Added: {product_name} — ₹{price} (image: {filename})")
            )

        self.stdout.write(self.style.SUCCESS(f"Done. Created {created} guitar products."))

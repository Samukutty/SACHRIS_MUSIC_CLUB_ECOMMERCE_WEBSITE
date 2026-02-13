from django.core.management.base import BaseCommand, CommandError

from Admin.product.models import productModel


class Command(BaseCommand):
    help = "Remove a product (and its uploaded images) by id or exact name."

    def add_arguments(self, parser):
        parser.add_argument("--id", type=int, help="Product ID to delete")
        parser.add_argument("--name", type=str, help="Exact product name to delete")
        parser.add_argument(
            "--yes",
            action="store_true",
            help="Do not prompt for confirmation",
        )

    def handle(self, *args, **options):
        product_id = options.get("id")
        name = options.get("name")
        assume_yes = options.get("yes", False)

        if not product_id and not name:
            raise CommandError("Provide either --id or --name")
        if product_id and name:
            raise CommandError("Provide only one of --id or --name (not both)")

        if product_id:
            qs = productModel.objects.filter(id=product_id)
        else:
            qs = productModel.objects.filter(productname=name)

        count = qs.count()
        if count == 0:
            raise CommandError("No matching product found.")
        if count > 1:
            raise CommandError(
                f"Multiple products matched ({count}). Use --id to delete a specific one."
            )

        product = qs.first()
        self.stdout.write(f"Found product: id={product.id} name={product.productname!r}")

        if not assume_yes:
            confirm = input("Type DELETE to confirm: ").strip()
            if confirm != "DELETE":
                self.stdout.write("Cancelled.")
                return

        product.delete()
        self.stdout.write(self.style.SUCCESS("Deleted."))


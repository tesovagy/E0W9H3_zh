class WarehouseOB:
    def __init__(self):
        self.products = {}
        self.thresholds_ob = {}

    def add_product_ob(self, name, quantity, threshold=10):
        self.products[name] = quantity
        self.thresholds_ob[name] = threshold

    def remove_product_ob(self, name):
        if name in self.products:
            del self.products[name]
            if name in self.thresholds_ob:
                del self.thresholds_ob[name]
            return True
        return False

    def update_threshold_ob(self, name, threshold):
        if name in self.products:
            self.thresholds_ob[name] = threshold
            return True
        return False

    def get_threshold_ob(self, name):
        return self.thresholds_ob.get(name, 10)  # Alapértelmezett: 10

    def list_products_ob(self):
        return self.products

    def search_product_ob(self, keyword):
        results = {}
        for product, quantity in self.products.items():
            if keyword.lower() in product.lower():
                results[product] = quantity
        return results

    def get_stock_status_ob(self, name, quantity):
        threshold = self.get_threshold_ob(name)

        if quantity <= threshold:
            return "low"
        elif quantity <= threshold * 1.5:
            return "medium"
        elif quantity >= threshold * 4:
            return "high"
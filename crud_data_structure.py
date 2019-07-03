# CRUD with feature:
# - Unique id
# - Show
# - Insert
# - Update
# - Delete


class Product:

    def __init__(self, data_store=[]):
        self.data_store = data_store

    def __is_exist(self, idn):
        idn_list = [v['idn'] for v in self.data_store]
        exist = (idn in idn_list)
        idx = (idn_list.index(idn) if exist else None)
        return exist, idx

    def show(self):
        for data in self.data_store:
            yield "ID: {} | Product Name: {} | Stock: {} ".format(data['idn'], data['name'], data['stock'])

    def insert(self, idn, name, stock=1):
        if not self._Product__is_exist(idn)[0]:
            self.data_store.append({"idn": idn, "name": name, "stock": stock})
        else:
            data = self.data_store[self._Product__is_exist(idn)[1]]
            data = {
                'idn': idn,
                'name': data['name'],
                'stock': data['stock'] + stock
            }

    def update(self, idn, name=None, stock=None):
        if self._Product__is_exist(idn)[0]:
            data = self.data_store[self._Product__is_exist(idn)[1]]
            data.update({
                'idn': idn,
                'name': (name if name else data['name']),
                'stock': (stock if stock else data['stock'])
            })

    def delete(self, idn):
        data = self.data_store[self._Product__is_exist(idn)[1]]
        self.data_store.remove(data)


initial_data = [{"idn": 1, "name": "Tester", "stock": 4}]


product = Product(initial_data)
print(product.data_store)
print("")

product.insert(23, "Tester 23")
print(product.data_store)
print("")

product.insert(22, "Tester 22")
print(product.data_store)
print("")

product.insert(22, "Tester 22") # To test dupclicated data
print(product.data_store)
print("")

product.update(22, name="Tester 22 -- Updated")
print(product.data_store)
print("")

product.delete(1)
print(product.data_store)
print("")

for data in product.show():
    print(data)
print("")

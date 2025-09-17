from main import app

import category_op as cat


app.add_url_rule('/addCategory',view_func=cat.addCategory,methods=["GET","POST"])
app.add_url_rule('/ShowAllCategory',view_func=cat.showAllCategory,methods=["GET"])
app.add_url_rule('/deleteCategory',view_func=cat.deleteCategory,methods=["GET","POST"])
app.add_url_rule('/updateCategory',view_func=cat.updateCategory,methods=["GET","POST"])
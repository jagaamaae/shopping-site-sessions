"""Ubermelon shopping application Flask server.

Provides web interface for browsing melons, seeing detail about a melon, and
put melons in a shopping cart.

Authors: Joel Burton, Christian Fernandez, Meggie Mahnken, Katie Byers.
"""

from flask import Flask, session, render_template, redirect, flash, request
import jinja2

import melons

app = Flask(__name__)

# A secret key is needed to use Flask sessioning features
app.secret_key = 'this-should-be-something-unguessable'

# Normally, if you refer to an undefined variable in a Jinja template,
# Jinja silently ignores this. This makes debugging difficult, so we'll
# set an attribute of the Jinja environment that says to make this an
# error.
app.jinja_env.undefined = jinja2.StrictUndefined

# This configuration option makes the Flask interactive debugger
# more useful (you should remove this line in production though)
app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = True


@app.route("/")
def index():
    """Return homepage."""

    return render_template("homepage.html")


@app.route("/melons")
def list_melons():
    """Return page showing all the melons ubermelon has to offer"""

    melon_list = melons.get_all()
    return render_template("all_melons.html",
                           melon_list=melon_list)


@app.route("/melon/<melon_id>")
def show_melon(melon_id):
    """Return page showing the details of a given melon.

    Show all info about a melon. Also, provide a button to buy that melon.
    """

    melon = melons.get_by_id(melon_id)
    print(melon)
    return render_template("melon_details.html",
                           display_melon=melon)


@app.route("/cart")
def show_shopping_cart():
    """Display content of shopping cart."""

    melon_list =[]
    order_total = 0
    # username = session["user"]
    cart = session.get("cart", {})
    # {'cart': {'cren': 3, 'water': 1,'winter':3, 'golden':1},
    # 'user': 'marisa',
    # 'fav_animal': 'cat'}
    for melon_id, quantity in cart.items():
        melon = melons.get_by_id(melon_id)
        total_cost = quantity * melon.price
        order_total += total_cost
        melon.quantity = quantity
        melon.total_cost = total_cost
        melon_list.append(melon)

    return render_template("cart.html",
                           cart=melon_list,
                           order_total=order_total)
    # Make sure your function can also handle the case wherein no cart has
    # been added to the session

@app.route("/add_to_cart/<melon_id>")
def add_to_cart(melon_id):
    """Add a melon to cart and redirect to shopping cart page.

    When a melon is added to the cart, redirect browser to the shopping cart
    page and display a confirmation message: 'Melon successfully added to
    cart'."""

    session["cart"].setdefault("cart",[]).append(melon_id)
    flash("Success!")
    # TODO: Finish shopping cart functionality

    # The logic here should be something like:
    #
    # - check if a "cart" exists in the session, and create one (an empty
    #   dictionary keyed to the string "cart") if not
    # - check if the desired melon id is the cart, and if not, put it in
    # - increment the count for that melon id by 1
    # - flash a success message
    # - redirect the user to the cart page
    # Redirect to shopping cart page
    return redirect("/cart")

@app.route("/login", methods=["GET"])

def show_login():
    """Show login form."""
    def show_login():
        if 'logged_in_customer_email' not in session: 
            return render_template("login.html")
        flash("You are logged in")
        return redirect("/melons")


@app.route("/login", methods=["POST"])
def process_login():
    
    """Log user into site.

    Find the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session.
    """
    username = request.form.get("username")
    password  = request.form.get ("password")

    if username in customers and customers[email].pw == password:
        session['logged_in_customer_email'] = email
        flash("Success! You are logged in.")
        return redirect("/melons")
    elif email in customers and customers[email].pw != password:
        flash("Incorrect password.")
        return redirect("/login")
    else:
        flash("No such email.")
        return redirect("/login")


@app.route("/checkout")
def checkout():
    """Checkout customer, process payment, and ship melons."""

    # For now, we'll just provide a warning. Completing this is beyond the
    # scope of this exercise.

    flash("Sorry! Checkout will be implemented in a future version.")
    return redirect("/melons")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

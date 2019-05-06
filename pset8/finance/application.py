import os
from re import search
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    portfolio = db.execute("SELECT shares, symbol FROM own where user_id = :id", \
                            id=session["user_id"])

    # check if the portfolio exists, otherwise render an empty template
    if not portfolio:
        render_template("index.html")

    # get cash of the user
    cash = db.execute("SELECT cash FROM users where id = :id", \
                            id=session["user_id"])

    # add stock's current price to each stock in portfolio list
    total = 0.0
    for stock in portfolio:
        s = lookup(stock["symbol"])
        stock["price"] = usd(s["price"])
        stock["total"] = usd(s["price"] * stock["shares"])
        total += float(stock["total"].replace(",","").strip("$"))

    # get the total of the portfolio
    total = usd(cash[0]["cash"] + total)
    cash = usd(cash[0]["cash"])

    return render_template("index.html", portfolio=portfolio, cash=cash, total=total)

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    # Buy shares of stock
    # User reached route via POST
    if request.method == 'POST':

        # get the user input
        try:
            if request.args.get("symbol"):
                stock = lookup(request.args.get("symbol"))
                shares = int(1)
            elif request.form.get("symbol"):
                stock = lookup(request.form.get("symbol"))
                shares = int(request.form.get("shares"))
        except (TypeError, ValueError) as error:
            return apology("Invalid values.", 403)

        money = db.execute("SELECT cash FROM users WHERE id = :id", \
                            id=session["user_id"])

        # check if stock is valid
        if not stock:
            return apology("Invalid stock.", 403)

        cost = shares * stock["price"]

        if not shares > 0:
            return apology("Please enter a positive value.", 403)

        # check if the user have sufficient money to purchase
        try:
            if cost > float(money[0]["cash"]):
                return apology("Insufficient fund.", 403)
        except NameError:
            return apology("User's money does not exist.", 403)

        # record a transaction for the purchase
        db.execute("INSERT INTO buy (shares, symbol, cost, id, datetime) \
                                VALUES (:shares, :symbol, :cost, :user_id, CURRENT_TIMESTAMP)", \
                                shares=shares, \
                                symbol=stock["symbol"], \
                                cost=usd(cost), \
                                user_id=session["user_id"])

        # subtract the cost from the user's cash
        db.execute("UPDATE users SET cash = cash - :cash WHERE id = :id", \
                        cash = cost, id=session["user_id"])

        # Select user shares of that symbol
        user_shares = db.execute("SELECT shares FROM own \
                           WHERE user_id = :user_id AND symbol=:symbol", \
                           user_id=session["user_id"], symbol=stock["symbol"])

        # if user doesn't has shares of that symbol, create new stock object
        if not user_shares:
            db.execute("INSERT INTO own (user_id, shares, symbol) \
                        VALUES (:user_id, :shares, :symbol)", \
                        user_id=session["user_id"], \
                        shares=shares, symbol=stock["symbol"])

        # Else increment the shares count
        else:
            shares_total = user_shares[0]["shares"] + shares
            db.execute("UPDATE own SET shares=:shares \
                        WHERE user_id=:id AND symbol=:symbol", \
                        shares=shares_total, id=session["user_id"], \
                        symbol=stock["symbol"])

        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/check", methods=["GET"])
def check():

    """ Return true if username available, else false, in JSON format."""
    username = str(request.args.get("username"))

    if len(username) < 1:
        return jsonify("The username must be at least 1 character long.")

    # Get the username from the database if it exists.
    username2 = db.execute("SELECT username from users WHERE username = :username", \
                            username=username)

    if username2:
        if username == username2[0]["username"]:
            return jsonify("The username is not available.")

    # Return true if the username is not duplicate
    return jsonify(True)


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    buy = db.execute("SELECT shares, symbol, cost, datetime FROM buy WHERE id = :id", \
                        id=session["user_id"])
    sell = db.execute("SELECT shares, symbol, cost, datetime FROM sell WHERE id = :id", \
                        id=session["user_id"])

    return render_template("history.html", buy=buy, sell=sell)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    # User reached route via POST
    if request.method == 'POST':

        # get the quote from the user and look it up
        quoted = lookup(request.form.get("symbol"))

        # check if quote is valid
        if not quoted:
            return apology("Invalid quote", 403)

        quoted['price'] = usd(quoted['price'])

        return render_template("quoted.html", quote=quoted)

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("Must provide username", 400)

        # ensure password was submitted
        if not request.form.get("password"):
            return apology("Must provide password", 400)

        # ensure password and verified password is the same
        elif request.form.get("password") != request.form.get("password2"):
            return apology("Password doesn't match", 400)

        # insert a new user / password into the db
        else :
            registered = db.execute("INSERT INTO users (username, hash) \
                                    VALUES (:username, :hash)", \
                                    username=request.form.get("username"), \
                                    hash=generate_password_hash(request.form.get("password")))

        # remember which user has logged in
        session["user_id"] = registered

        # redirect user to home page
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/add", methods=["POST"])
@login_required
def add():
    """Add more money"""
    if request.method == "POST":

        money = request.args.get("money")

        try:
            if money < 0:
                return apology("Invalid money.", 300)
        except ValueError:
            return apology("Invalid money value.", 300)

        db.execute("UPDATE users SET cash = cash + :cash WHERE id = :id", \
                    cash = money, \
                    id=session["user_id"])

    return redirect("/")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "GET":

        # fetch the user portfolio and create a select list
        portfolio = db.execute("SELECT * FROM own WHERE user_id = :user_id", \
                                user_id=session["user_id"])

        if not portfolio:
            return apology("User portfolio does not exist.", 403)

        return render_template("sell.html", portfolio=portfolio)

    if request.method == "POST":

        # get the user input
        try:
            if request.args.get("symbol"):
                stock = request.args.get("symbol")
                share_sold = int(1)
            elif request.form.get("portfolio"):
                stock = request.form.get("portfolio")
                share_sold = int(request.form.get("shares"))
        except (TypeError, ValueError) as error:
            return apology("Invalid values.", 403)

        # fetch the symbol and shares to be sold
        stock = db.execute("SELECT * from own WHERE user_id = :user_id AND symbol = :stock", \
                            user_id=session["user_id"], \
                            stock=stock)

        # shares to be sold
        share_own = int(stock[0]["shares"])

        # ensure user input for shares doesn't exceed what he owns
        try:
            if share_own < share_sold or share_sold < 0:
                return apology("Incorrect shares.", 300)
        except (ValueError, TypeError) as error:
            return apology("Incorrect shares.", 300)

        # single stock current price
        price = lookup(stock[0]["symbol"])
        price = price["price"] * share_sold

        # add money to user cash and remove the stock owned
        db.execute("UPDATE users SET cash = cash + :cash WHERE id = :id", \
                        cash = price, \
                        id=session["user_id"])

        # remove the stock from the table "own", otherwise, decrement shares
        if share_own == share_sold:
            db.execute("DELETE from own WHERE symbol = :symbol AND user_id = :id", \
                        symbol=stock[0]["symbol"], id=session["user_id"])
        else:
            db.execute("UPDATE own SET shares = shares - :shares WHERE \
                        symbol = :symbol AND user_id = :id", \
                        shares=share_sold, \
                        symbol=stock[0]["symbol"], \
                        id=session["user_id"])

        db.execute("INSERT INTO sell (shares, symbol, cost, id, datetime) \
                                VALUES (:shares, :symbol, :cost, :user_id, CURRENT_TIMESTAMP)", \
                                shares=share_sold, \
                                symbol=stock[0]["symbol"], \
                                cost=usd(price), \
                                user_id=session["user_id"])

        return redirect("/")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

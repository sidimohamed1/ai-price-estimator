from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import pandas as pd
import difflib

app = FastAPI()

# ربط الملفات الثابتة والقوالب
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# تحميل قاعدة بيانات المنتجات
df = pd.read_csv("products.csv")

@app.get("/", response_class=HTMLResponse)
def get_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/", response_class=HTMLResponse)
def estimate_price(request: Request, product_name: str = Form(...)):
    product_name = product_name.lower().strip()
    price = None

    # نحاول نلاقيه في الداتا مباشرة
    if product_name in df['name'].str.lower().values:
        price = df[df['name'].str.lower() == product_name]['price'].values[0]
    else:
        # نحاول نلاقي أقرب منتج مشابه
        closest = difflib.get_close_matches(product_name, df['name'].str.lower().values, n=1)
        if closest:
            price = df[df['name'].str.lower() == closest[0]]['price'].values[0]

    return templates.TemplateResponse("index.html", {"request": request, "price": price, "product": product_name})

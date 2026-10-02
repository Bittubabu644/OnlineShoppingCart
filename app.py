from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import random
import smtplib
import requests

from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv(
    "FLASK_SECRET_KEY",
    "online-shopping-cart-secret-key"
)


# =========================================================
# PRODUCT DATA
# =========================================================

products = [
    {
        "id": 1,
        "name": "Premium Laptop",
        "category": "Laptops",
        "price": 49999,
        "original_price": 64999,
        "discount": 23,
        "rating": 4.5,
        "reviews": 1250,
        "image": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=600",
        "description": "Powerful laptop suitable for students, programming and everyday work.",
        "specifications": [
            "Intel Core i5 Processor",
            "16GB RAM",
            "512GB SSD",
            "15.6 inch Full HD Display",
            "Windows 11"
        ],
        "stock": 10
    },
    {
        "id": 2,
        "name": "Smartphone Pro",
        "category": "Mobiles",
        "price": 19999,
        "original_price": 24999,
        "discount": 20,
        "rating": 4.4,
        "reviews": 2380,
        "image": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=600",
        "description": "Modern smartphone with powerful performance and excellent camera.",
        "specifications": [
            "6.5 inch AMOLED Display",
            "8GB RAM",
            "128GB Storage",
            "5000mAh Battery",
            "50MP Camera"
        ],
        "stock": 20
    },
    {
        "id": 3,
        "name": "Wireless Headphones",
        "category": "Accessories",
        "price": 2499,
        "original_price": 3999,
        "discount": 38,
        "rating": 4.3,
        "reviews": 980,
        "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=600",
        "description": "Comfortable wireless headphones with powerful sound.",
        "specifications": [
            "Bluetooth 5.3",
            "40 Hours Battery",
            "Noise Reduction",
            "Fast Charging",
            "Built-in Microphone"
        ],
        "stock": 30
    },
    {
        "id": 4,
        "name": "Wireless Mouse",
        "category": "Accessories",
        "price": 599,
        "original_price": 999,
        "discount": 40,
        "rating": 4.2,
        "reviews": 650,
        "image": "https://images.unsplash.com/photo-1527814050087-3793815479db?w=600",
        "description": "Ergonomic wireless mouse for laptop and desktop users.",
        "specifications": [
            "Wireless Connection",
            "Ergonomic Design",
            "Adjustable DPI",
            "Long Battery Life"
        ],
        "stock": 50
    },
    {
        "id": 5,
        "name": "Smart Watch",
        "category": "Accessories",
        "price": 2999,
        "original_price": 4999,
        "discount": 40,
        "rating": 4.1,
        "reviews": 720,
        "image": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600",
        "description": "Stylish smartwatch for fitness and daily activities.",
        "specifications": [
            "AMOLED Display",
            "Heart Rate Monitor",
            "Sleep Tracking",
            "Water Resistant",
            "7 Days Battery"
        ],
        "stock": 25
    },
    {
        "id": 6,
        "name": "Running Shoes",
        "category": "Fashion",
        "price": 1799,
        "original_price": 2999,
        "discount": 40,
        "rating": 4.3,
        "reviews": 430,
        "image": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=600",
        "description": "Comfortable running shoes designed for everyday use.",
        "specifications": [
            "Lightweight Design",
            "Breathable Material",
            "Cushioned Sole",
            "Anti-Slip Sole"
        ],
        "stock": 40
    },

    {

        "id": 7,
        "name": "Men's Casual Shirt",
        "category": "Fashion",
        "price": 899,
        "original_price": 1499,
        "discount": 40,
        "rating": 4.2,
        "reviews": 320,
        "image": "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=600",
        "description": "Comfortable casual shirt suitable for everyday wear.",
        "specifications": [
            "100% Cotton",
            "Regular Fit",
            "Machine Washable",
            "Comfortable Fabric"
        ],

        "stock": 35
    },

    {
        "id": 8,
        "name": "Bluetooth Speaker",
        "category": "Electronics",
        "price": 1599,
        "original_price": 2499,
        "discount": 36,
        "rating": 4.4,
        "reviews": 850,
        "image": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=600",
        "description": "Portable Bluetooth speaker with powerful audio.",
        "specifications": [
            "Bluetooth 5.0",
            "12 Hours Battery",
            "Water Resistant",
            "Portable Design"
        ],
        "stock": 28
    },


    {
        "id": 201,
        "name": "Dell Inspiron 15 Laptop",
        "category": "Laptops",
        "price": 52999,
        "original_price": 64999,
        "discount": 18,
        "rating": 4.4,
        "reviews": 1540,
        "image": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=600",
        "description": "Reliable laptop for students, office work and programming.",
        "specifications": ["Intel Core i5", "16GB RAM", "512GB SSD", "15.6 inch Display"],
        "stock": 15
    },

    {
        "id": 202,
        "name": "HP Pavilion Gaming Laptop",
        "category": "Laptops",
        "price": 67999,
        "original_price": 79999,
        "discount": 15,
        "rating": 4.5,
        "reviews": 980,
        "image": "https://images.unsplash.com/photo-1603302576837-37561b2e2302?w=600",
        "description": "Powerful gaming and performance laptop.",
        "specifications": ["Intel Core i7", "16GB RAM", "512GB SSD", "RTX Graphics"],
        "stock": 12
    },

    {
        "id": 203,
        "name": "Lenovo IdeaPad Slim",
        "category": "Laptops",
        "price": 44999,
        "original_price": 54999,
        "discount": 18,
        "rating": 4.3,
        "reviews": 870,
        "image": "https://images.unsplash.com/photo-1531297484001-80022131f5a1?w=600",
        "description": "Slim and lightweight laptop for daily work.",
        "specifications": ["Ryzen 5", "8GB RAM", "512GB SSD", "Full HD Display"],
        "stock": 20
    },

    {
        "id": 204,
        "name": "MacBook Air",
        "category": "Laptops",
        "price": 89999,
        "original_price": 99999,
        "discount": 10,
        "rating": 4.8,
        "reviews": 2100,
        "image": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=600",
        "description": "Premium laptop with excellent performance and battery life.",
        "specifications": ["Apple Silicon", "8GB RAM", "256GB SSD", "Retina Display"],
        "stock": 8
    },

    {
        "id": 205,
        "name": "ASUS Vivobook 15",
        "category": "Laptops",
        "price": 47999,
        "original_price": 57999,
        "discount": 17,
        "rating": 4.4,
        "reviews": 1150,
        "image": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=600",
        "description": "Modern laptop for students and professionals.",
        "specifications": ["Intel Core i5", "8GB RAM", "512GB SSD", "15.6 inch Display"],
        "stock": 18
    },

    {
        "id": 206,
        "name": "OnePlus 13",
        "category": "Mobiles",
        "price": 69999,
        "original_price": 79999,
        "discount": 12,
        "rating": 4.6,
        "reviews": 1780,
        "image": "https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=600",
        "description": "Flagship smartphone with powerful performance.",
        "specifications": ["AMOLED Display", "12GB RAM", "256GB Storage", "5G"],
        "stock": 15
    },

    {
        "id": 207,
        "name": "Google Pixel 9",
        "category": "Mobiles",
        "price": 64999,
        "original_price": 74999,
        "discount": 13,
        "rating": 4.5,
        "reviews": 1320,
        "image": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=600",
        "description": "Premium smartphone with an excellent camera.",
        "specifications": ["OLED Display", "12GB RAM", "256GB Storage", "50MP Camera"],
        "stock": 14
    },

    {
        "id": 208,
        "name": "Redmi Note 14 Pro",
        "category": "Mobiles",
        "price": 24999,
        "original_price": 29999,
        "discount": 17,
        "rating": 4.4,
        "reviews": 2450,
        "image": "https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=600",
        "description": "Feature-packed smartphone at an affordable price.",
        "specifications": ["AMOLED Display", "8GB RAM", "256GB Storage", "108MP Camera"],
        "stock": 30
    },

    {
        "id": 209,
        "name": "Realme GT Smartphone",
        "category": "Mobiles",
        "price": 32999,
        "original_price": 39999,
        "discount": 18,
        "rating": 4.3,
        "reviews": 1120,
        "image": "https://images.unsplash.com/photo-1523206489230-c012c64b2b48?w=600",
        "description": "Fast smartphone designed for performance and gaming.",
        "specifications": ["120Hz Display", "12GB RAM", "256GB Storage", "5G"],
        "stock": 22
    },

    {
        "id": 210,
        "name": "Samsung Galaxy A55",
        "category": "Mobiles",
        "price": 29999,
        "original_price": 34999,
        "discount": 14,
        "rating": 4.4,
        "reviews": 1640,
        "image": "https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?w=600",
        "description": "Stylish Samsung smartphone with great display.",
        "specifications": ["Super AMOLED", "8GB RAM", "128GB Storage", "50MP Camera"],
        "stock": 25
    },

    {
        "id": 211,
        "name": "JBL Bluetooth Speaker",
        "category": "Audio",
        "price": 3499,
        "original_price": 4999,
        "discount": 30,
        "rating": 4.6,
        "reviews": 1890,
        "image": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=600",
        "description": "Portable speaker with powerful bass and clear sound.",
        "specifications": ["Bluetooth 5.0", "20 Hours Battery", "Water Resistant", "Deep Bass"],
        "stock": 35
    },

    {
        "id": 212,
        "name": "Boat Rockerz Headphones",
        "category": "Audio",
        "price": 1799,
        "original_price": 2999,
        "discount": 40,
        "rating": 4.3,
        "reviews": 3120,
        "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=600",
        "description": "Affordable wireless headphones for music and calls.",
        "specifications": ["Bluetooth", "40 Hours Battery", "Fast Charging", "Microphone"],
        "stock": 45
    },

    {
        "id": 213,
        "name": "Premium Soundbar",
        "category": "Audio",
        "price": 7999,
        "original_price": 9999,
        "discount": 20,
        "rating": 4.5,
        "reviews": 720,
        "image": "https://images.unsplash.com/photo-1545454675-3531b543be5d?w=600",
        "description": "Home theatre soundbar for immersive audio.",
        "specifications": ["Dolby Audio", "Bluetooth", "HDMI", "Wireless Subwoofer"],
        "stock": 10
    },

    {
        "id": 214,
        "name": "Wireless Earbuds Pro",
        "category": "Audio",
        "price": 2999,
        "original_price": 4999,
        "discount": 40,
        "rating": 4.4,
        "reviews": 1420,
        "image": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=600",
        "description": "Compact wireless earbuds with clear audio.",
        "specifications": ["ANC", "Bluetooth 5.3", "30 Hours Battery", "Touch Controls"],
        "stock": 40
    },

    {
        "id": 215,
        "name": "USB Gaming Headset",
        "category": "Gaming",
        "price": 2499,
        "original_price": 3999,
        "discount": 38,
        "rating": 4.4,
        "reviews": 890,
        "image": "https://images.unsplash.com/photo-1599669454699-248893623440?w=600",
        "description": "Gaming headset with microphone and surround sound.",
        "specifications": ["7.1 Surround Sound", "RGB Lighting", "USB", "Noise Cancelling Mic"],
        "stock": 25
    },

    {
        "id": 216,
        "name": "Gaming Mouse RGB",
        "category": "Gaming",
        "price": 1299,
        "original_price": 1999,
        "discount": 35,
        "rating": 4.5,
        "reviews": 1340,
        "image": "https://images.unsplash.com/photo-1527814050087-3793815479db?w=600",
        "description": "High precision RGB gaming mouse.",
        "specifications": ["12000 DPI", "RGB Lighting", "6 Buttons", "Ergonomic Design"],
        "stock": 50
    },

    {
        "id": 217,
        "name": "Gaming Monitor 24 Inch",
        "category": "Gaming",
        "price": 12999,
        "original_price": 16999,
        "discount": 24,
        "rating": 4.5,
        "reviews": 680,
        "image": "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=600",
        "description": "Fast gaming monitor with smooth refresh rate.",
        "specifications": ["24 inch Full HD", "144Hz Refresh Rate", "1ms Response", "HDMI"],
        "stock": 15
    },

    {
        "id": 218,
        "name": "Mechanical Gaming Keyboard",
        "category": "Gaming",
        "price": 3999,
        "original_price": 5999,
        "discount": 33,
        "rating": 4.6,
        "reviews": 950,
        "image": "https://images.unsplash.com/photo-1595225476474-87563907a212?w=600",
        "description": "Mechanical keyboard designed for gaming.",
        "specifications": ["Mechanical Keys", "RGB", "Anti Ghosting", "Gaming Mode"],
        "stock": 30
    },

    {
        "id": 219,
        "name": "Smart LED TV 43 Inch",
        "category": "Television",
        "price": 29999,
        "original_price": 39999,
        "discount": 25,
        "rating": 4.5,
        "reviews": 1240,
        "image": "https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?w=600",
        "description": "4K smart television for your home entertainment.",
        "specifications": ["43 inch 4K", "HDR", "WiFi", "Smart TV"],
        "stock": 12
    },

    {
        "id": 220,
        "name": "Smart LED TV 55 Inch",
        "category": "Television",
        "price": 42999,
        "original_price": 54999,
        "discount": 22,
        "rating": 4.6,
        "reviews": 870,
        "image": "https://images.unsplash.com/photo-1461151304267-38535e780c79?w=600",
        "description": "Large 4K smart television with vibrant colors.",
        "specifications": ["55 inch 4K", "Dolby Audio", "HDR10", "WiFi"],
        "stock": 8
    },

    {
        "id": 221,
        "name": "Smart Air Conditioner",
        "category": "Home Appliances",
        "price": 35999,
        "original_price": 44999,
        "discount": 20,
        "rating": 4.4,
        "reviews": 560,
        "image": "https://images.unsplash.com/photo-1631545806609-7e5a6f5a8f72?w=600",
        "description": "Energy efficient smart air conditioner.",
        "specifications": ["1.5 Ton", "5 Star", "Inverter", "WiFi Control"],
        "stock": 10
    },

    {
        "id": 222,
        "name": "Front Load Washing Machine",
        "category": "Home Appliances",
        "price": 28999,
        "original_price": 36999,
        "discount": 22,
        "rating": 4.4,
        "reviews": 740,
        "image": "https://images.unsplash.com/photo-1626806787461-102c1bfaaea1?w=600",
        "description": "Modern washing machine with multiple wash programs.",
        "specifications": ["7 KG Capacity", "Fully Automatic", "Inverter Motor", "Multiple Modes"],
        "stock": 10
    },

    {
        "id": 223,
        "name": "Microwave Oven",
        "category": "Home Appliances",
        "price": 8999,
        "original_price": 11999,
        "discount": 25,
        "rating": 4.3,
        "reviews": 610,
        "image": "https://images.unsplash.com/photo-1585659722983-3a675dabf23d?w=600",
        "description": "Compact microwave oven for modern kitchens.",
        "specifications": ["25 L Capacity", "Convection", "Auto Cook", "Digital Display"],
        "stock": 18
    },

    {
        "id": 224,
        "name": "Air Fryer",
        "category": "Kitchen",
        "price": 3999,
        "original_price": 5999,
        "discount": 33,
        "rating": 4.5,
        "reviews": 920,
        "image": "https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec?w=600",
        "description": "Healthy cooking air fryer with digital controls.",
        "specifications": ["5 L Capacity", "Digital Controls", "Timer", "Temperature Control"],
        "stock": 25
    },

    {
        "id": 225,
        "name": "Mixer Grinder",
        "category": "Kitchen",
        "price": 2499,
        "original_price": 3499,
        "discount": 29,
        "rating": 4.3,
        "reviews": 810,
        "image": "https://images.unsplash.com/photo-1570222094114-d054a817e56b?w=600",
        "description": "Powerful mixer grinder for everyday kitchen use.",
        "specifications": ["750W Motor", "3 Jars", "Stainless Steel Blades", "Overload Protection"],
        "stock": 30
    },

    {
        "id": 226,
        "name": "Coffee Maker",
        "category": "Kitchen",
        "price": 2999,
        "original_price": 4499,
        "discount": 33,
        "rating": 4.4,
        "reviews": 520,
        "image": "https://images.unsplash.com/photo-1517668808822-9ebb02f2a0e6?w=600",
        "description": "Easy-to-use coffee maker for home and office.",
        "specifications": ["1.5 L Capacity", "Fast Brewing", "Easy Cleaning", "Auto Shut Off"],
        "stock": 20
    },

    {
        "id": 227,
        "name": "Men's Denim Jacket",
        "category": "Fashion",
        "price": 1999,
        "original_price": 2999,
        "discount": 33,
        "rating": 4.3,
        "reviews": 480,
        "image": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=600",
        "description": "Classic denim jacket for casual styling.",
        "specifications": ["Denim Fabric", "Regular Fit", "Full Sleeves", "Multiple Pockets"],
        "stock": 35
    },

    {
        "id": 228,
        "name": "Women's Handbag",
        "category": "Fashion",
        "price": 1599,
        "original_price": 2499,
        "discount": 36,
        "rating": 4.4,
        "reviews": 670,
        "image": "https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=600",
        "description": "Stylish handbag suitable for everyday use.",
        "specifications": ["Premium Material", "Multiple Compartments", "Shoulder Strap", "Lightweight"],
        "stock": 28
    },

    {
        "id": 229,
        "name": "Running Sports Shoes",
        "category": "Fashion",
        "price": 2299,
        "original_price": 3499,
        "discount": 34,
        "rating": 4.5,
        "reviews": 890,
        "image": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=600",
        "description": "Lightweight sports shoes for running and workouts.",
        "specifications": ["Lightweight", "Cushioned Sole", "Breathable", "Anti Slip"],
        "stock": 40
    },

    {
        "id": 230,
        "name": "Classic Leather Wallet",
        "category": "Fashion",
        "price": 799,
        "original_price": 1299,
        "discount": 38,
        "rating": 4.3,
        "reviews": 720,
        "image": "https://images.unsplash.com/photo-1627123424574-724758594e93?w=600",
        "description": "Classic wallet with multiple card and cash slots.",
        "specifications": ["Leather Material", "Multiple Card Slots", "Cash Compartment", "Compact Design"],
        "stock": 50
    },

    {
        "id": 231,
        "name": "Travel Backpack",
        "category": "Bags",
        "price": 1799,
        "original_price": 2999,
        "discount": 40,
        "rating": 4.5,
        "reviews": 610,
        "image": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=600",
        "description": "Large travel backpack with laptop compartment.",
        "specifications": ["40 L Capacity", "Laptop Compartment", "Water Resistant", "Travel Friendly"],
        "stock": 25
    },

    {
        "id": 232,
        "name": "School Backpack",
        "category": "Bags",
        "price": 999,
        "original_price": 1599,
        "discount": 38,
        "rating": 4.2,
        "reviews": 450,
        "image": "https://images.unsplash.com/photo-1581605405669-fcdf81165afa?w=600",
        "description": "Durable backpack for school and college.",
        "specifications": ["Large Compartments", "Water Resistant", "Padded Straps", "Lightweight"],
        "stock": 45
    },

    {
        "id": 233,
        "name": "Digital Smart Watch",
        "category": "Wearables",
        "price": 3499,
        "original_price": 4999,
        "discount": 30,
        "rating": 4.4,
        "reviews": 1120,
        "image": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600",
        "description": "Smartwatch with health and fitness tracking features.",
        "specifications": ["AMOLED Display", "Heart Rate", "Sleep Tracking", "Bluetooth Calling"],
        "stock": 30
    },

    {
        "id": 234,
        "name": "Fitness Smart Band",
        "category": "Wearables",
        "price": 1499,
        "original_price": 2499,
        "discount": 40,
        "rating": 4.2,
        "reviews": 930,
        "image": "https://images.unsplash.com/photo-1576243345690-4e4b79b63288?w=600",
        "description": "Lightweight fitness band for daily activity tracking.",
        "specifications": ["Activity Tracking", "Heart Rate", "Sleep Monitoring", "Water Resistant"],
        "stock": 50
    },

    {
        "id": 235,
        "name": "Power Bank 20000mAh",
        "category": "Accessories",
        "price": 1799,
        "original_price": 2999,
        "discount": 40,
        "rating": 4.4,
        "reviews": 1760,
        "image": "https://images.unsplash.com/photo-1609592424848-ef4c7e8b8f1d?w=600",
        "description": "High capacity power bank with fast charging.",
        "specifications": ["20000mAh", "Fast Charging", "Dual USB", "LED Indicator"],
        "stock": 40
    },

    {
        "id": 236,
        "name": "USB-C Fast Charger",
        "category": "Accessories",
        "price": 899,
        "original_price": 1499,
        "discount": 40,
        "rating": 4.3,
        "reviews": 1250,
        "image": "https://images.unsplash.com/photo-1583863788434-e58a36330cf0?w=600",
        "description": "Compact fast charger for smartphones and other devices.",
        "specifications": ["33W Fast Charging", "USB-C", "Safety Protection", "Compact Design"],
        "stock": 60
    },

    {
        "id": 237,
        "name": "Laptop Backpack",
        "category": "Bags",
        "price": 1499,
        "original_price": 2499,
        "discount": 40,
        "rating": 4.5,
        "reviews": 820,
        "image": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=600",
        "description": "Professional laptop backpack for students and office users.",
        "specifications": ["15.6 inch Laptop Slot", "Water Resistant", "USB Port", "Padded Straps"],
        "stock": 35
    },

    {
        "id": 238,
        "name": "Study Table Lamp",
        "category": "Home",
        "price": 799,
        "original_price": 1299,
        "discount": 38,
        "rating": 4.4,
        "reviews": 530,
        "image": "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=600",
        "description": "Modern LED study lamp with adjustable brightness.",
        "specifications": ["LED Light", "3 Brightness Modes", "Flexible Neck", "USB Powered"],
        "stock": 40
    },

    {
        "id": 239,
        "name": "LED Room Light",
        "category": "Home",
        "price": 1299,
        "original_price": 1999,
        "discount": 35,
        "rating": 4.3,
        "reviews": 410,
        "image": "https://images.unsplash.com/photo-1540932239986-30128078f3c5?w=600",
        "description": "Modern LED light for bedroom and living room.",
        "specifications": ["Energy Efficient", "Bright LED", "Long Life", "Easy Installation"],
        "stock": 30
    },

    {
        "id": 240,
        "name": "Portable Electric Fan",
        "category": "Home",
        "price": 1199,
        "original_price": 1799,
        "discount": 33,
        "rating": 4.2,
        "reviews": 380,
        "image": "https://images.unsplash.com/photo-1523830299227-84d3e0f7c6c1?w=600",
        "description": "Compact portable fan for home, office and travel.",
        "specifications": ["USB Powered", "3 Speed Modes", "Portable", "Quiet Operation"],
        "stock": 35
    },

]


# =========================================================
# EMAIL NOTIFICATION
# =========================================================

def send_order_email(order_id, customer, items, total, payment):
    """Send a complete new-order notification to the shop owner's email."""
    sender = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASSWORD")
    receiver = os.getenv("OWNER_EMAIL")
    smtp_host = os.getenv("EMAIL_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("EMAIL_PORT", "587"))

    if not sender or not password or not receiver:
        print("Email notification skipped: EMAIL_USER, EMAIL_PASSWORD or OWNER_EMAIL is missing in .env")
        return False

    product_text = "\n".join(
        f"- {item['product']['name']} x {item['quantity']} = Rs. {item['subtotal']}"
        for item in items
    )

    message_body = f"""
NEW ORDER RECEIVED

Order ID: {order_id}

CUSTOMER
Name: {customer['name']}
Mobile: {customer['mobile']}
Email: {customer['email']}

DELIVERY ADDRESS
{customer['address']}
{customer['city']}, {customer['state']} - {customer['pincode']}

PRODUCTS
{product_text}

PAYMENT METHOD
{payment}

TOTAL AMOUNT
Rs. {total}
"""

    msg = EmailMessage()
    msg["Subject"] = f"New Order - {order_id}"
    msg["From"] = sender
    msg["To"] = receiver
    msg.set_content(message_body)

    try:
        with smtplib.SMTP(smtp_host, smtp_port, timeout=20) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(sender, password)
            server.send_message(msg)

        print("Order email sent successfully.")
        return True

    except Exception as error:
        print("Email sending failed:", error)
        return False


# =========================================================
# WHATSAPP NOTIFICATION
# =========================================================

def send_whatsapp_notification(order_id, customer, total, payment):
    """
    Sends WhatsApp notification using Meta WhatsApp Cloud API.

    Configure:
    WHATSAPP_TOKEN
    WHATSAPP_PHONE_NUMBER_ID
    OWNER_PHONE
    """

    token = os.getenv("WHATSAPP_TOKEN")
    phone_number_id = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
    shop_number = os.getenv("OWNER_PHONE")

    if not token or not phone_number_id or not shop_number:
        print("WhatsApp notification skipped: API settings not configured.")
        return False

    url = (
        f"https://graph.facebook.com/v23.0/"
        f"{phone_number_id}/messages"
    )

    message = (
        f"NEW ORDER\n\n"
        f"Order ID: {order_id}\n"
        f"Customer: {customer['name']}\n"
        f"Mobile: {customer['mobile']}\n"
        f"Total: Rs. {total}\n"
        f"Payment: {payment}\n\n"
        f"Address: {customer['city']}, "
        f"{customer['state']} - {customer['pincode']}"
    )

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    data = {
        "messaging_product": "whatsapp",
        "to": shop_number,
        "type": "text",
        "text": {
            "body": message
        }
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            json=data,
            timeout=15
        )

        if response.ok:
            print("WhatsApp notification sent.")
            return True

        print("WhatsApp API error:", response.text)
        return False

    except Exception as error:
        print("WhatsApp sending failed:", error)
        return False

#PART2

# =========================================================
# HELPER FUNCTIONS
# =========================================================

def get_product(product_id):
    """Find a product by its ID."""
    for product in products:
        if product["id"] == product_id:
            return product
    return None


def get_cart_items():
    """Convert session cart into detailed product/cart data."""
    cart = session.get("cart", {})
    items = []
    total = 0

    for product_id, quantity in cart.items():
        product = get_product(int(product_id))

        if product and quantity > 0:
            subtotal = product["price"] * quantity

            items.append({
                "product": product,
                "quantity": quantity,
                "subtotal": subtotal
            })

            total += subtotal

    return items, total


def generate_order_id():
    """Generate a simple order ID."""
    return "ORD" + str(random.randint(100000, 999999))


# =========================================================
# HOME PAGE
# =========================================================

@app.route("/")
def home():
    categories = sorted(
        list(set(product["category"] for product in products))
    )

    return render_template(
        "index.html",
        products=products,
        categories=categories
    )


# =========================================================
# PRODUCT DETAILS
# =========================================================

@app.route("/product/<int:product_id>")
def product_details(product_id):
    product = get_product(product_id)

    if not product:
        flash("Product not found.")
        return redirect(url_for("home"))

    return render_template(
        "product.html",
        product=product
    )


# =========================================================
# SEARCH
# =========================================================

@app.route("/search")
def search():
    query = request.args.get("q", "").strip().lower()

    if not query:
        return redirect(url_for("home"))

    results = []

    for product in products:
        if (
            query in product["name"].lower()
            or query in product["category"].lower()
            or query in product["description"].lower()
        ):
            results.append(product)

    categories = sorted(
        list(set(product["category"] for product in products))
    )

    return render_template(
        "index.html",
        products=results,
        categories=categories,
        search_query=query
    )


# =========================================================
# CATEGORY
# =========================================================

@app.route("/category/<category_name>")
def category(category_name):
    selected_products = [
        product
        for product in products
        if product["category"].lower() == category_name.lower()
    ]

    categories = sorted(
        list(set(product["category"] for product in products))
    )

    return render_template(
        "index.html",
        products=selected_products,
        categories=categories,
        selected_category=category_name
    )


# =========================================================
# ADD TO CART
# =========================================================

@app.route("/add-to-cart/<int:product_id>", methods=["POST", "GET"])
def add_to_cart(product_id):
    product = get_product(product_id)

    if not product:
        flash("Product not found.")
        return redirect(url_for("home"))

    cart = session.get("cart", {})

    product_key = str(product_id)

    current_quantity = int(cart.get(product_key, 0))

    if current_quantity >= product["stock"]:
        flash("Sorry, this product is out of stock.")
        return redirect(request.referrer or url_for("home"))

    cart[product_key] = current_quantity + 1

    session["cart"] = cart
    session.modified = True

    flash(f"{product['name']} added to cart.")

    return redirect(request.referrer or url_for("home"))


# =========================================================
# UPDATE CART
# =========================================================

@app.route("/update-cart/<int:product_id>", methods=["POST"])
def update_cart(product_id):
    product = get_product(product_id)

    if not product:
        flash("Product not found.")
        return redirect(url_for("cart"))

    quantity = request.form.get("quantity", "1")

    try:
        quantity = int(quantity)
    except ValueError:
        quantity = 1

    cart = session.get("cart", {})
    product_key = str(product_id)

    if quantity <= 0:
        cart.pop(product_key, None)

    elif quantity > product["stock"]:
        flash(f"Only {product['stock']} units are available.")
        cart[product_key] = product["stock"]

    else:
        cart[product_key] = quantity

    session["cart"] = cart
    session.modified = True

    return redirect(url_for("cart"))


# =========================================================
# REMOVE FROM CART
# =========================================================

@app.route("/remove-from-cart/<int:product_id>")
def remove_from_cart(product_id):
    cart = session.get("cart", {})

    cart.pop(str(product_id), None)

    session["cart"] = cart
    session.modified = True

    flash("Product removed from cart.")

    return redirect(url_for("cart"))


# =========================================================
# CART PAGE
# =========================================================

@app.route("/cart")
def cart():
    items, total = get_cart_items()

    return render_template(
        "cart.html",
        items=items,
        total=total
    )


# =========================================================
# CHECKOUT PAGE
# =========================================================

@app.route("/checkout")
def checkout():
    items, total = get_cart_items()

    if not items:
        flash("Your cart is empty.")
        return redirect(url_for("cart"))

    return render_template(
        "checkout.html",
        items=items,
        total=total
    )


# =========================================================
# PLACE ORDER
# =========================================================

@app.route("/place-order", methods=["POST"])
def place_order():

    items, total = get_cart_items()

    if not items:
        flash("Your cart is empty.")
        return redirect(url_for("cart"))

    # -----------------------------------------------------
    # CUSTOMER DETAILS
    # -----------------------------------------------------

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    mobile = request.form.get("mobile", "").strip()

    address = request.form.get("address", "").strip()
    city = request.form.get("city", "").strip()
    state = request.form.get("state", "").strip()
    pincode = request.form.get("pincode", "").strip()

    payment = request.form.get(
        "payment",
        request.form.get("payment_method", "Cash on Delivery")
    )

    # -----------------------------------------------------
    # VALIDATION
    # -----------------------------------------------------

    if not name:
        flash("Please enter your name.")
        return redirect(url_for("checkout"))

    if not email:
        flash("Please enter your email.")
        return redirect(url_for("checkout"))

    if "@" not in email or "." not in email.split("@")[-1]:
        flash("Please enter a valid email address.")
        return redirect(url_for("checkout"))

    if not mobile:
        flash("Please enter your mobile number.")
        return redirect(url_for("checkout"))

    if not address:
        flash("Please enter your address.")
        return redirect(url_for("checkout"))

    if not city:
        flash("Please enter your city.")
        return redirect(url_for("checkout"))

    if not state:
        flash("Please enter your state.")
        return redirect(url_for("checkout"))

    if not pincode:
        flash("Please enter your pincode.")
        return redirect(url_for("checkout"))

    # -----------------------------------------------------
    # CREATE CUSTOMER DATA
    # -----------------------------------------------------

    customer = {
        "name": name,
        "email": email,
        "mobile": mobile,
        "address": address,
        "city": city,
        "state": state,
        "pincode": pincode
    }

    # -----------------------------------------------------
    # CREATE ORDER ID
    # -----------------------------------------------------

    order_id = generate_order_id()

    # -----------------------------------------------------
    # SEND EMAIL
    # -----------------------------------------------------

    send_order_email(
        order_id,
        customer,
        items,
        total,
        payment
    )

    # -----------------------------------------------------
    # SEND WHATSAPP
    # -----------------------------------------------------

    send_whatsapp_notification(
        order_id,
        customer,
        total,
        payment
    )

    # -----------------------------------------------------
    # SAVE LAST ORDER IN SESSION
    # -----------------------------------------------------

    session["last_order"] = {
        "order_id": order_id,
        "customer": customer,
        "items": items,
        "total": total,
        "payment": payment
    }

    # Empty cart after successful order
    session["cart"] = {}

    session.modified = True

    return redirect(url_for("order_success"))


# PART3

# =========================================================
# ORDER SUCCESS PAGE
# =========================================================

@app.route("/order-success")
def order_success():
    order = session.get("last_order")

    if not order:
        flash("No recent order found.")
        return redirect(url_for("home"))

    return render_template(
        "order_success.html",
        order=order
    )


# =========================================================
# MY ACCOUNT / ORDERS
# =========================================================

@app.route("/orders")
def orders():
    order = session.get("last_order")

    return render_template(
        "orders.html",
        order=order
    )


# =========================================================
# CLEAR CART
# =========================================================

@app.route("/clear-cart")
def clear_cart():
    session["cart"] = {}
    session.modified = True

    flash("Cart cleared successfully.")

    return redirect(url_for("cart"))


# =========================================================
# API - PRODUCT LIST
# =========================================================

@app.route("/api/products")
def api_products():
    return {
        "success": True,
        "count": len(products),
        "products": products
    }


# =========================================================
# API - SINGLE PRODUCT
# =========================================================

@app.route("/api/products/<int:product_id>")
def api_product(product_id):
    product = get_product(product_id)

    if not product:
        return {
            "success": False,
            "message": "Product not found"
        }, 404

    return {
        "success": True,
        "product": product
    }


# =========================================================
# API - CART
# =========================================================

@app.route("/api/cart")
def api_cart():
    items, total = get_cart_items()

    cart_items = []

    for item in items:
        cart_items.append({
            "id": item["product"]["id"],
            "name": item["product"]["name"],
            "price": item["product"]["price"],
            "quantity": item["quantity"],
            "subtotal": item["subtotal"],
            "image": item["product"]["image"]
        })

    return {
        "success": True,
        "items": cart_items,
        "total": total
    }


# =========================================================
# API - SEARCH
# =========================================================

@app.route("/api/search")
def api_search():
    query = request.args.get("q", "").strip().lower()

    if not query:
        return {
            "success": True,
            "products": []
        }

    results = []

    for product in products:
        if (
            query in product["name"].lower()
            or query in product["category"].lower()
            or query in product["description"].lower()
        ):
            results.append(product)

    return {
        "success": True,
        "query": query,
        "count": len(results),
        "products": results
    }


# =========================================================
# LOGIN PAGE
# =========================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        if not email or not password:
            flash("Please enter email and password.")
            return redirect(url_for("login"))

        # Demo login system
        session["user"] = {
            "email": email
        }

        flash("Login successful.")

        return redirect(url_for("home"))

    return render_template("login.html")


# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
def logout():

    session.pop("user", None)

    flash("You have been logged out.")

    return redirect(url_for("home"))


# =========================================================
# REGISTER
# =========================================================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        if not name or not email or not password:
            flash("Please fill all registration fields.")
            return redirect(url_for("register"))

        session["user"] = {
            "name": name,
            "email": email
        }

        flash("Registration successful.")

        return redirect(url_for("home"))

    return render_template("register.html")


# =========================================================
# PROFILE
# =========================================================

@app.route("/profile")
def profile():

    user = session.get("user")

    if not user:
        flash("Please login first.")
        return redirect(url_for("login"))

    return render_template(
        "profile.html",
        user=user
    )


# =========================================================
# WISHLIST
# =========================================================

@app.route("/wishlist")
def wishlist():

    wishlist = session.get("wishlist", [])

    wishlist_products = []

    for product_id in wishlist:
        product = get_product(int(product_id))

        if product:
            wishlist_products.append(product)

    return render_template(
        "wishlist.html",
        products=wishlist_products
    )


@app.route("/add-to-wishlist/<int:product_id>")
def add_to_wishlist(product_id):

    product = get_product(product_id)

    if not product:
        flash("Product not found.")
        return redirect(url_for("home"))

    wishlist = session.get("wishlist", [])

    if str(product_id) not in wishlist:
        wishlist.append(str(product_id))

    session["wishlist"] = wishlist
    session.modified = True

    flash(f"{product['name']} added to wishlist.")

    return redirect(request.referrer or url_for("home"))


@app.route("/remove-from-wishlist/<int:product_id>")
def remove_from_wishlist(product_id):

    wishlist = session.get("wishlist", [])

    if str(product_id) in wishlist:
        wishlist.remove(str(product_id))

    session["wishlist"] = wishlist
    session.modified = True

    flash("Product removed from wishlist.")

    return redirect(url_for("wishlist"))


# =========================================================
# CONTACT PAGE
# =========================================================

@app.route("/contact", methods=["GET", "POST"])
def contact():

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()

        if not name or not email or not message:
            flash("Please fill all fields.")
            return redirect(url_for("contact"))

        # Contact form is accepted.
        # Email notification can be connected later.

        flash("Thank you! Your message has been received.")

        return redirect(url_for("contact"))

    return render_template("contact.html")


# =========================================================
# ABOUT PAGE
# =========================================================

@app.route("/about")
def about():
    return render_template("about.html")


# =========================================================
# 404 ERROR
# =========================================================

@app.errorhandler(404)
def page_not_found(error):
    return render_template(
        "404.html"
    ), 404


# =========================================================
# 500 ERROR
# =========================================================

@app.errorhandler(500)
def internal_server_error(error):
    return render_template(
        "500.html"
    ), 500


# =========================================================
# CONTEXT PROCESSOR
# =========================================================

@app.context_processor
def inject_cart_count():

    cart = session.get("cart", {})

    cart_count = 0

    for quantity in cart.values():
        try:
            cart_count += int(quantity)
        except (ValueError, TypeError):
            pass

    return {
        "cart_count": cart_count
    }

# PART 4
# =========================================================
# APPLICATION START
# =========================================================

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=True
    )
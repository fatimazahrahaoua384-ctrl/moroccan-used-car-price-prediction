🇬🇧 English | [🇫🇷 Français](README.fr.md)
# moroccan-used-car-price-prediction
End-to-end machine learning project predicting used car prices in Morocco: data collection, scikit-learn/XGBoost modeling, FastAPI backend, Next.js frontend, Docker deployment.

## 1. Problem

In Morocco, it is hard to know whether the asking price of a used car is fair. Buyers risk overpaying, and sellers may set a price that does not match the market. This project is for **both**: buyers who want to check a listing, and sellers who want to estimate the value of their car.

## 2. Goal

A web application where the user enters a car's characteristics and gets a price estimate in Moroccan dirhams, from a model trained on a dataset of used car listings.

## 3. Target variable

The **selling price** of the car, in Moroccan dirhams (MAD).

## 4. Expected input features

- Brand and model
- Year of first registration
- Mileage
- Fuel type (petrol, diesel, hybrid, etc.)
- Transmission (manual, automatic)
- Fiscal horsepower (CV)
- City
- Number of doors (if available)

## 5. Success metric (initial hypothesis)

I will use the **MAE** (mean absolute error) because it is easy to interpret: on average, the model is off by X dirhams.
Initial target: **MAE below 10% of the median price** in the dataset. This target will be revised after exploratory analysis.
The model must also beat a simple baseline (linear regression).

## 6. Out of scope (version 1)

- Other vehicle types (motorcycles, vans, trucks)
- Analysis of listing photos
- Price prediction for new cars

## Data

Source: *to be completed once the dataset is chosen* (name, link, size, date, license).

## Planned stack

Python, pandas, scikit-learn, XGBoost, FastAPI, Next.js, Docker.

## Status

Work in progress.
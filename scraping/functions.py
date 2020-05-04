from geopy.geocoders import Nominatim
from geopy.exc import GeocoderServiceError


def ask_for_criteria(n):
    print(f"\nFor city # {n}")
    city = input("City name: ")
    prov = input("Province name in 2 letters: ")
    max_price = int(input("Max price: "))
    min_beds = int(input("Min number of beds: "))
    min_year_built = int(input("Year built from: "))

    return (city, prov, max_price, min_beds, min_year_built)


def url_builder(pg, city, prov, price, bed, year):
    return f"https://www.rew.ca/properties/areas/{city}-{prov}/page/{pg}?" \
           f"is_exact_bedrooms=false&list_price_to={price}&" \
           f"num_bedrooms={bed}&only_open_house=0&only_virtual_tour=0&" \
           f"searchable_id=361&searchable_type=Geography&" \
           f"year_built_from={year}"


# retries in case of prone service errors
# credit: https://gis.stackexchange.com/questions/173569/avoid-time-out-error-nominatim-geopy-open-street-maps
def do_geocode(address, attempt=1, max_attempts=5):
    try:
        return Nominatim().geocode(address)
    except GeocoderServiceError:
        if attempt <= max_attempts:
            return do_geocode(address, attempt=attempt+1)
        raise

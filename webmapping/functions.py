import numpy


def calc_thresholds(data):
    l1_threshold = numpy.percentile(data, 100 / 3)
    l2_threshold = numpy.percentile(data, 200 / 3)

    return l1_threshold, l2_threshold


def make_html(row):
    html1 = """
    <font size="1.8"><b> $ %s / sq<sup>2</sup> </b></font>
    <br><font size="1.5">Total Area: %s sq<sup>2</sup></font>
    <br><font size="1.5">Price: %s </font>
    <br><font size="1.5"> %s Beds, %s Baths </font>
    <br><font size="1.5"><a href= """

    html2 = """
    > %s </a></font>
    """

    return html1 % (str(int(row["$/sq"])), str(row["Area"]), row["Price"],
                    str(row["Bed"]), str(row["Bath"])) + "\"https://www." \
           + row["Link"] + "\"" + html2 % row["Address"]


def color_producer(psq, l1_threshold, l2_threshold):
    if psq < l1_threshold:
        return 'green'
    elif l1_threshold <= psq < l2_threshold:
        return 'orange'
    else:
        return 'red'

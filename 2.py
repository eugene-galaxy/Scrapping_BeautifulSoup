from concurrent.futures import ThreadPoolExecutor

def process_item(item):
    # Perform some processing on the item
    print(item)

# Create an iterable of input values
input_values = list(range(1, 1000))

# Create a ThreadPoolExecutor
with ThreadPoolExecutor() as executor:
    # Execute process_item concurrently on each input value
    results = executor.map(process_item, input_values)

    # Process the results
    # for result in results:
        # Do something with the result
        # ...

import json
import toml
import timeit
start = timeit.default_timer()

with open('text.json', 'r') as f:
    data = json.load(f)

with open('output2.toml', 'w') as f:
    toml.dump(data, f)
end = timeit.default_timer()
print(f"Время выполнения: {(end - start)*100} секунд*100")


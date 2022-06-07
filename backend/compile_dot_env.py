INCLUDED_FILES = (
    "../ops/docker/envs/postgres.env",
    "../ops/docker/envs/redis.env",
    "../ops/docker/envs/build.env",
    "../ops/docker/envs/app.env",
    "./.env.local",
)
OUTPUT_FILE = "./.env"

output = ""
for filepath in INCLUDED_FILES:
    with open(filepath, "r") as file:
        content = file.read()
        output += content + "\n"


with open(OUTPUT_FILE, "w") as file:
    file.write(output)

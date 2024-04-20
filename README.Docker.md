# `docker pull dadahsueh/kookie`

#### [Kookie Docker Image](https://hub.docker.com/r/dadahsueh/kookie)


## 📝 Table of Contents

- [Prerequisites](#prerequisites)
- [Running](#running)
- [Building](#building)
- [Resources](#resources)

## 1️⃣ Prerequisites <a name = "prerequisites"></a>
Need to have docker desktop installed [Mac](https://docs.docker.com/desktop/install/mac-install/) / [Windows](https://docs.docker.com/desktop/install/windows-install/) / [Linux](https://docs.docker.com/desktop/install/linux-install/).

Need the `.env` file or manually enter `--env xxx=xxx`

If you want to clone the repo or you can just `touch .env` at the working directory:
```
git clone https://github.com/dadahsueh/kookie.git
cd kookie
mv .env.template .env
```

Configure the `.env` if you are want to use the `--env-file` method
```
TOKEN=BOT_TOKEN_HERE
CONTAINER_NAME=kookie-runner
ADMIN_USERS=["635507656"]
BOT_NAME=KOOKIE
BOT_VERSION=v0.0.1
MUSIC_STATUS=[";"]
```

## 🎈 Running <a name = "running"></a>

Pull the docker image
```
docker pull dadahsueh/kookie
```

use configured file
```
docker run -i --env-file .env --name kookie-container kookie
```
or manually set `--env xxx=xxx` or short `-e xxx=xxx`
```
docker run -i --env TOKEN=Your_Token_Here --name kookie-container kookie
```

optional `--restart always`, for more info check [Docker Manual](https://docs.docker.com/manuals/).

## 🔨 Building <a name = "building"></a>

Clone git repo
```
git clone https://github.com/dadahsueh/kookie.git
cd kookie
mv .env.template .env
```
Build
```
docker build --no-cache=true -t kookie:latest .
```
Then go see [Running](#running) if you want to run the bot.

<br>

### (Optional) Push tag
if you want to push to a docker repo, rename to your repo:tag
```
docker image tag kookie:latest dadahsueh/kookie:latest
```
push to your repo:tag
```
docker push dadahsueh/kookie:latest
```
remove image with old name
```
docker rmi kookie
```

<br>

## 💭 Resources <a name = "resources"></a>

- [Docker Manual](https://docs.docker.com/manuals/)

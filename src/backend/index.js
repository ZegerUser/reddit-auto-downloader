const fs = require("fs/promises");
const express = require("express");
const cors = require("cors");
const bodyParser = require('body-parser')

const app = express();
app.use(cors());
app.use(bodyParser.urlencoded({ extended: false }))
app.use(bodyParser.json())

app.get("/config", async (req, res) => {
    configData = await fs.readFile("config.json");
    res.json(JSON.parse(configData));
})

app.put("/config/add", async(req, res) => {
    const sub = req.body.sub;
    if(!sub){
        return res.sendStatus(400)
    }
    configData = JSON.parse(await fs.readFile("config.json"));
    subs = sub.split('\n')
    for(let i = 0; i < subs.length; i++){
        if(!configData["subreddits"].includes(subs[i])){
            configData["subreddits"].push(subs[i])
        }
    }
    fs.writeFile("config.json", JSON.stringify(configData))
    res.sendStatus(201)
})
app.delete("/config/remove", async(req, res) =>{
    const sub = req.body.sub;
    if(!sub){
        return res.sendStatus(400)
    }
    configData = JSON.parse(await fs.readFile("config.json"));
    if(!configData["subreddits"].includes(sub)){
        return res.sendStatus(404)
    }
    const index = configData["subreddits"].indexOf(sub);
    if (index > -1) { // only splice array when item is found
        configData["subreddits"].splice(index, 1); // 2nd parameter means remove one item only
    }
    fs.writeFile("config.json", JSON.stringify(configData))
    res.sendStatus(200)
})

app.listen(3000, () => console.log("API started ..."));
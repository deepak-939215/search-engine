const express = require('express');
const ejs = require('ejs');
const path = require('path');
var fs = require('fs');
const {spawn} = require('child_process');

const app = express();
app.use(express.json());
app.set("view engine", "ejs");
app.use(express.static(path.join(__dirname, "/public")));
app.use(express.static(path.join(__dirname, "/views")));

const PORT = process.env.PORT || 3000;

app.get('/', (req,res)=>{
    res.render("index");
})
app.get('/search', (req,res)=>{
    const query = req.query;
    const question = query.question;
    var ans = [];
    const python = spawn('python', ['server.py', question]);
    python.stdout.on('data', function (data) {
        ans.push(data);
    });
    python.on('close', (code) => {
        res.json(ans.join(""));
    });
});

app.listen(PORT,()=>{
    console.log("Server is running on port"+PORT);
});
from flask import Flask, render_template_string, request, jsonify, g, redirect
import base64
import sqlite3
import json
import random
import os
import requests
from bs4 import BeautifulSoup
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_mail import Mail, Message
from flask_simple_geoip import SimpleGeoIP
from datetime import datetime
app = Flask(__name__)

PROXIES = [
    {
        "http":"http://id9096:lynxproxies@194.110.172.185:3486",
        "https":"http://id9096:lynxproxies@194.110.172.185:3486"
    },
    {
        "http":"http://id9096:lynxproxies@194.110.172.186:3486",
        "https":"http://id9096:lynxproxies@194.110.172.186:3486"
    },
    {
        "http":"http://id9096:lynxproxies@194.110.172.176:3486",
        "https":"http://id9096:lynxproxies@194.110.172.176:3486"
    },
    {
        "http":"http://id9096:lynxproxies@194.110.172.174:3486",
        "https":"http://id9096:lynxproxies@194.110.172.174:3486"
    },
    {
        "http":"http://id9096:lynxproxies@194.110.172.140:3486",
        "https":"http://id9096:lynxproxies@194.110.172.140:3486"
    },
    {
        "http":"http://id9096:lynxproxies@194.110.172.153:3486",
        "https":"http://id9096:lynxproxies@194.110.172.153:3486"
    },
    {
        "http":"http://id9096:lynxproxies@194.110.172.154:3486",
        "https":"http://id9096:lynxproxies@194.110.172.154:3486"
    },
    {
        "http":"http://id9096:lynxproxies@194.110.172.143:3486",
        "https":"http://id9096:lynxproxies@194.110.172.143:3486"
    },
    {
        "http":"http://id9096:lynxproxies@194.110.172.169:3486",
        "https":"http://id9096:lynxproxies@194.110.172.169:3486"
    },
    {
        "http":"http://id9096:lynxproxies@194.110.172.184:3486",
        "https":"http://id9096:lynxproxies@194.110.172.184:3486"
    },
    {
        "http":"http://id9096:lynxproxies@194.110.172.152:3486",
        "https":"http://id9096:lynxproxies@194.110.172.152:3486"
    },
    {
        "http":"http://id9096:lynxproxies@194.110.172.180:3486",
        "https":"http://id9096:lynxproxies@194.110.172.180:3486"
    },
    {
        "http":"http://id9096:lynxproxies@194.110.172.145:3486",
        "https":"http://id9096:lynxproxies@194.110.172.145:3486"
    },
    {
        "http":"http://id9096:lynxproxies@194.110.172.175:3486",
        "https":"http://id9096:lynxproxies@194.110.172.175:3486"
    },
    {
        "http":"http://id9096:lynxproxies@194.110.172.160:3486",
        "https":"http://id9096:lynxproxies@194.110.172.160:3486"
    },
    {
        "http":"http://id9096:lynxproxies@194.110.172.151:3486",
        "https":"http://id9096:lynxproxies@194.110.172.151:3486"
    },
    {
        "http":"http://id9096:lynxproxies@194.110.172.165:3486",
        "https":"http://id9096:lynxproxies@194.110.172.165:3486"
    },
    {
        "http":"http://id9096:lynxproxies@194.110.172.172:3486",
        "https":"http://id9096:lynxproxies@194.110.172.172:3486"
    },
    {
        "http":"http://id9096:lynxproxies@194.110.172.167:3486",
        "https":"http://id9096:lynxproxies@194.110.172.167:3486"
    },
    {
        "http":"http://id9096:lynxproxies@194.110.172.157:3486",
        "https":"http://id9096:lynxproxies@194.110.172.157:3486"
    },
    {
        "http":"http://id9096:lynxproxies@194.110.172.161:3486",
        "https":"http://id9096:lynxproxies@194.110.172.161:3486"
    },
    {
        "http":"http://id9096:lynxproxies@194.110.172.159:3486",
        "https":"http://id9096:lynxproxies@194.110.172.159:3486"
    },
    {
        "http":"http://id9096:lynxproxies@194.110.172.141:3486",
        "https":"http://id9096:lynxproxies@194.110.172.141:3486"
    },
    {
        "http":"http://id9096:lynxproxies@194.110.172.181:3486",
        "https":"http://id9096:lynxproxies@194.110.172.181:3486"
    },
    {
        "http":"http://id9096:lynxproxies@194.110.172.177:3486",
        "https":"http://id9096:lynxproxies@194.110.172.177:3486"
    },
    {
        "http":"http://id9096:lynxproxies@194.110.172.182:3486",
        "https":"http://id9096:lynxproxies@194.110.172.182:3486"
    },
    {
        "http":"http://id9096:lynxproxies@194.110.172.178:3486",
        "https":"http://id9096:lynxproxies@194.110.172.178:3486"
    },
    {
        "http":"http://id9096:lynxproxies@194.110.172.163:3486",
        "https":"http://id9096:lynxproxies@194.110.172.163:3486"
    },
    {
        "http":"http://id9096:lynxproxies@194.110.172.179:3486",
        "https":"http://id9096:lynxproxies@194.110.172.179:3486"
    },
    {
        "http":"http://id9096:lynxproxies@194.110.172.158:3486",
        "https":"http://id9096:lynxproxies@194.110.172.158:3486"
    },
    {
        "http":"http://id9096:lynxproxies@194.110.172.168:3486",
        "https":"http://id9096:lynxproxies@194.110.172.168:3486"
    },
    {
        "http":"http://id9096:lynxproxies@194.110.172.147:3486",
        "https":"http://id9096:lynxproxies@194.110.172.147:3486"
    },
    {
        "http":"http://id9096:lynxproxies@194.110.172.171:3486",
        "https":"http://id9096:lynxproxies@194.110.172.171:3486"
    },
    {
        "http":"http://id9096:lynxproxies@194.110.172.149:3486",
        "https":"http://id9096:lynxproxies@194.110.172.149:3486"
    },
    {
        "http":"http://id9096:lynxproxies@194.110.172.188:3486",
        "https":"http://id9096:lynxproxies@194.110.172.188:3486"
    },
    {
        "http":"http://id9096:lynxproxies@194.110.172.142:3486",
        "https":"http://id9096:lynxproxies@194.110.172.142:3486"
    },
    {
        "http":"http://id9096:lynxproxies@194.110.172.155:3486",
        "https":"http://id9096:lynxproxies@194.110.172.155:3486"
    },
    {
        "http":"http://id9096:lynxproxies@194.110.172.166:3486",
        "https":"http://id9096:lynxproxies@194.110.172.166:3486"
    },
    {
        "http":"http://id9096:lynxproxies@194.110.172.146:3486",
        "https":"http://id9096:lynxproxies@194.110.172.146:3486"
    },
    {
        "http":"http://id9096:lynxproxies@194.110.172.150:3486",
        "https":"http://id9096:lynxproxies@194.110.172.150:3486"
    },
    {
        "http":"http://id9096:lynxproxies@194.110.172.156:3486",
        "https":"http://id9096:lynxproxies@194.110.172.156:3486"
    },
    {
        "http":"http://id9096:lynxproxies@194.110.172.170:3486",
        "https":"http://id9096:lynxproxies@194.110.172.170:3486"
    },
    {
        "http":"http://id9096:lynxproxies@194.110.172.164:3486",
        "https":"http://id9096:lynxproxies@194.110.172.164:3486"
    },
    {
        "http":"http://id9096:lynxproxies@194.110.172.183:3486",
        "https":"http://id9096:lynxproxies@194.110.172.183:3486"
    },
    {
        "http":"http://id9096:lynxproxies@194.110.172.173:3486",
        "https":"http://id9096:lynxproxies@194.110.172.173:3486"
    },
    {
        "http":"http://id9096:lynxproxies@194.110.172.144:3486",
        "https":"http://id9096:lynxproxies@194.110.172.144:3486"
    },
    {
        "http":"http://id9096:lynxproxies@194.110.172.187:3486",
        "https":"http://id9096:lynxproxies@194.110.172.187:3486"
    },
    {
        "http":"http://id9096:lynxproxies@194.110.172.162:3486",
        "https":"http://id9096:lynxproxies@194.110.172.162:3486"
    },
    {
        "http":"http://id9096:lynxproxies@194.110.172.189:3486",
        "https":"http://id9096:lynxproxies@194.110.172.189:3486"
    },
    {
        "http":"http://id9096:lynxproxies@194.110.172.148:3486",
        "https":"http://id9096:lynxproxies@194.110.172.148:3486"
    }
]

app.config.update(GEOIPIFY_API_KEY=os.environ.get('GEOIPIFY_API_KEY'))
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


USERENV = os.environ.get('USER')
PASSWORDENV = os.environ.get('PASSWORD')
uri = os.environ.get('DATABASE_URL')



# app.config['MAIL_USERNAME'] = "novakk.dev@gmail.com"
# app.config['MAIL_PASSWORD'] = "Khushchau0503"
# USERENV = "NVK-VTT2YHC0IOGT9CKS"
# PASSWORDENV = "Khushchau0503"
# uri = "postgres://tutrgatgtlielh:fa9ca45ea7f32d7cb566d1315dae5405399408871897b750a04b93c99c8fea6f@ec2-34-249-247-7.eu-west-1.compute.amazonaws.com:5432/de6uk97j0a2kuo"



if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = uri

db = SQLAlchemy(app)
engine = create_engine(uri)
# simple_geoip = SimpleGeoIP(app)

userURLS = {
    "VTT2-YHC0-IOGT-9CKS":{
        "STORE":"",
        "URL":"",
        "NONCE":""
    }
}
numberorletter = [0,1]
LETTERS = ['A', 'B', 'C', 'D', 'E','F', 'G', 'H', 'I', 'J', 'K','L', 'M', 'N', 'O', 'P', 'Q','R', 'S', 'T', 'U','V', 'W', 'X', 'Y', 'Z']
NUMBERS = ['0','1','2','3','4','5','6','7','8','9','10']
def createID(length):
    IDARR = []
    for i in range(length):
        if random.choice(numberorletter) == 1:
            IDARR.append(random.choice(LETTERS))
        else:
            IDARR.append(random.choice(NUMBERS))
    return ''.join(IDARR)


def gmailGen():
    html_str = """
        <body style="background-color:#000000" ></body>
        <style>
            div{
                text-align:center;
            }
            textarea{
                width:45vw;
                height:50vh;
                text-align:center;
                font-size:20;
                -webkit-box-sizing:border-box; 
            }
            input{
                text-align:center;
                width:9vw;
                height: 7vh;
                font-size: 30;
                border: none !important;
                color: black;
                background-color:white;
                border-radius: 0px;
                margin:0 10px 0 0;
                -webkit-box-sizing:border-box; 

            }
            ::placeholder {
                color: black !important;
                opacity: 1;
            }

            @media only screen and (max-width: 1400px) {
                textarea{
                    width:70vw;
                    height:40vh;
                    text-align:center;
                    font-size:28;
                    -webkit-box-sizing:border-box; 
                }
                input{
                    text-align:center;
                    width:15vw;
                    height: 10vh;
                    font-size: 35;
                    border: none !important;
                    color: black;
                    border-radius: 0px;
                    background-color:white;
                    -webkit-box-sizing:border-box; 
                    
                }
            }

            div::-webkit-scrollbar {
                display: none;
                position: absolute;
            }
            button:hover {box-shadow: 0px 1px 5px 5px #8A0379;}
            input:hover {box-shadow: 0px 1px 5px 5px #8A0379;}
            textarea:hover{box-shadow: 0px 1px 5px 5px #8A0379;}


        
        </style>
        <div>
            <br><br><br><br>
            <textarea type='text' class='newaddressbox' id="newaddressbox" rows="10000000" cols="3000000" style="overflow:auto" value="" spellcheck="false"></textarea>
            <br><br>
            <input autocomplete="off" id="loopamount" type='text' class="loopamount" value="" placeholder="amount" spellcheck="false">
            <input type="submit" class="jig-button" id="jigbutton" onclick="generategmails()" value="generate"/>
            <input type="submit" class="clear-button" id="clear-output" onclick="cleartext()" value="clear" disabled/>
            <input type="submit" class="export-button" id="export" onclick="exporttotext()" value='export' disabled/>
        </div>


        <script type='text/javascript'>
            function exporttotext(){
                if (document.getElementById('newaddressbox').value.length > 1){
                    let a = document.createElement('a');
                    a.href = "data:application/octet-stream,"+encodeURIComponent(document.getElementById('newaddressbox').value);
                    a.download = 'generatedgmails.txt';
                    a.click();
                }
            }
            function cleartext(){
                document.getElementById('newaddressbox').value = ''
            }
            function getRandomInt(min, max) {
                return Math.floor(Math.random() * (max - min)) + min;
            }
            function randomname(){
                var firstnames = ['Elizabeth', 'Peter', 'Christine', 'Robert', 'Jacob', 'Edward', 'Julia', 'Abdul', 'Sandra', 'Nathan', 'Christina', 'Andre', 'Marilyn', 'Allison', 'Luis', 'Raymond', 'Lynn', 'Arthur', 'Gladys', 'Vickie', 'Sylvester', 'Kathleen', 'Ellen', 'Faustina', 'Ruth', 'James', 'Raquel', 'Veronica', 'John', 'Dedra', 'Derrick', 'Emily', 'William', 'Rosemary', 'Hallie', 'Gregg', 'Olin', 'Allen', 'Glen', 'Daniel', 'Guy', 'Chris', 'Claudia', 'Joshua', 'Michael', 'Brandon', 'Jimmy', 'Judy', 'Leo', 'Erin', 'Sylvia', 'Danielle', 'Teresa', 'Mary', 'Ailene', 'Martin', 'Yolanda', 'Julie', 'Nicole', 'Orville', 'Norma', 'Lorraine', 'Clara', 'Milton', 'Ruby', 'April', 'Thomas', 'Jonathan', 'Todd', 'Nelly', 'Anthony', 'Janet', 'Aaron', 'Tyrone', 'Russell', 'Vanessa', 'Santana', 'Donald', 'Jacquline', 'Carolyn', 'Mazie', 'Ben', 'Janice', 'Paul', 'Johnny', 'Richard', 'Lena', 'Ronnie', 'Ray', 'Joanne', 'Gregory', 'Wendy', 'David', 'Beulah', 'Martha', 'Jeff', 'Terrance', 'Rafael', 'Marissa', 'Victoria', 'Molly', 'Elva', 'Bobby', 'Ronald', 'Cecile', 'Barbara', 'Ida', 'Alicia', 'Michelle', 'Marge', 'Jamie', 'Forest', 'George', 'Bryant', 'Kathy', 'Angela', 'Melba', 'Lesli', 'Bryan', 'Jerry', 'Adalberto', 'Tabatha', 'Crystal', 'Alfred', 'Suzanne', 'Douglas', 'Meryl', 'Brian', 'Joel', 'Jennifer', 'Gene', 'Anne', 'Jean', 'Joann', 'Angel', 'Shirley', 'Kayla', 'Chester', 'Rodney', 'Shoshana', 'Terry', 'Sharon', 'Kami', 'Eugene', 'Alaina', 'Bobbie', 'Lawrence', 'Harriet', 'Chad', 'Tom', 'Anna', 'Gary', 'Kent', 'Kevin', 'Muriel', 'Buck', 'Glenn', 'Melissa', 'Timothy', 'Mark', 'Rebecca', 'Ada', 'Pam', 'Monica', 'Annette', 'Tonya', 'Jess', 'Nancy', 'Jon', 'Rachael', 'Joesph', 'Eva', 'Velva', 'Keila', 'Patricia', 'Garry', 'Steve', 'Natalie', 'Jeffery', 'Terrence', 'Carol', 'Gigi', 'Dylan', 'Susan', 'Steven', 'Mariko', 'Louise', 'Kyle', 'Darlene', 'Ling', 'Will', 'Joyce', 'Kelvin', 'Judith', 'Karen', 'Rupert', 'Cynthia', 'Bob', 'Augustus', 'Amy', 'Artie', 'Melanie', 'Kathryn', 'Juana', 'Hilda', 'Ethel', 'Frank', 'Joseph', 'Bernard', 'Brad', 'Nick', 'Alexander', 'Jessica', 'Matthew', 'Adriana', 'Cristy', 'Shawnna', 'Roberto', 'Kimberly', 'Luther', 'Inez', 'Terri', 'Howard', 'Krystal', 'Malcolm', 'Bradford', 'Leonard', 'Marilou', 'Billy', 'Everett', 'Valerie', 'Karmen', 'Charles', 'Marylee', 'Christopher', 'Pat', 'Betty', 'Olivia', 'Essie', 'Leigh', 'Cindy', 'Leslie', 'Alan', 'Cedric', 'Jessie', 'Andrea', 'Bernice', 'Ezekiel', 'Antoinette', 'Johnnie', 'Jason', 'Margie', 'Katherine', 'Rosemarie', 'Larry', 'Renita', 'Misty', 'Carl', 'Patrick', 'Randy', 'Bertha', 'Helen', 'Denise', 'Jonathon', 'Justine', 'Eric', 'Nellie', 'Wayne', 'Ester', 'Geralyn', 'Andrew', 'Ignacio', 'Lorie', 'Amanda', 'Stephen', 'Tim', 'Darnell', 'Marion', 'Domingo', 'Ian', 'Jacquie', 'Felicia', 'Summer', 'Terence', 'Marjorie', 'Shawna', 'Alice', 'Orlando', 'Roxie', 'Caroline', 'Mabel', 'May', 'Edith', 'Alexis', 'Napoleon', 'Sergio', 'Linda', 'Levi', 'Kendall', 'Jorge', 'Ashlie', 'Frances', 'Kay', 'Santina', 'Dolores', 'Laura', 'Armida', 'Albert', 'Sara', 'Jaime', 'Keith', 'Josephine', 'Marie', 'Iris', 'Loretta', 'Lionel', 'Tina', 'Donna', 'Hoyt', 'Morgan', 'Ollie', 'Evan', 'Lila', 'Samuel', 'Claude', 'Eddie', 'Cathy', 'Whitley', 'Alysha', 'Henry', 'Stephane', 'Maria', 'Latrice', 'Lillian', 'Joanna', 'Graham', 'Harold', 'Elmer', 'Madonna', 'Lela', 'Lisa', 'Mike', 'Bruce', 'Brittany', 'Kenyatta', 'Shana', 'Edgar', 'Tiffany', 'Carla', 'Gloria', 'Chase', 'Alex', 'Selma', 'Cory', 'Leanne', 'Chanelle', 'Adrienne', 'Lucy', 'Cheryl', 'Sally', 'Mildred', 'Carly', 'Alphonse', 'Holly', 'Andres', 'Manuela', 'Ralph', 'Ashley', 'Annie', 'Loyce', 'Heather', 'Blanca', 'Walter', 'Maureen', 'Nikki', 'Jody', 'Jacelyn', 'Miquel', 'Tiffani', 'Clement', 'Jesus', 'Spencer', 'Cheri', 'Lance', 'Vincent', 'Miriam', 'Theron', 'Kenneth', 'Barry', 'Eli', 'Brady', 'Charlotte', 'Harry', 'Hershel', 'Debbie', 'Abraham', 'Cassandra', 'Vivan', 'Dawn', 'Kelly', 'Dallas', 'Sarah', 'Ila', 'Roderick', 'Barney', 'Derek', 'Jaclyn', 'Clarice', 'Winifred', 'Stacy', 'Juan', 'Karl', 'Doyle', 'Lee', 'Jack', 'Jill', 'Theresa', 'Horace', 'Roger', 'Weldon', 'Thelma', 'Carrie', 'Carmen', 'Kim', 'Bill', 'Kristen', 'Michele', 'Kelley', 'Nicholas', 'Earl', 'Louis', 'Brent', 'Ryan', 'Rodger', 'Marlon', 'Justin', 'Francisco', 'Fred', 'Antonina', 'Laurie', 'Rachel', 'Ashli', 'Mathew', 'Beverly', 'Regan', 'Curtis', 'Jose', 'Carlos', 'Leda', 'Hazel', 'Demetra', 'Beatrice', 'Jenny', 'Tara', 'Florence', 'Penny', 'Mariela', 'Joan', 'Lindsay', 'Ernest', 'Maryann', 'Margaret', 'Jordan', 'Shannon', 'Gina', 'Brandi', 'Willie', 'Tyler', 'Lynne', 'Catherine', 'Robin', 'Donella', 'Drusilla', 'Mattie', 'Lan', 'Marcelina', 'Marvin', 'Dennise', 'Sheila', 'Eileen', 'Nia', 'Glenda', 'Kerri', 'Althea', 'Alberto', 'Jesse', 'Virginia', 'Dorothy', 'Son', 'Alvin', 'Dan', 'Terrie', 'Melvin', 'Moises', 'Cecil', 'Haydee', 'Tamesha', 'Julian', 'Bradley', 'Gerardo', 'Clifton', 'Patrica', 'Bailey', 'Leroy', 'Erica', 'Anita', 'Audrey', 'Callie', 'Yvonne', 'Shauna', 'Edna', 'Jimmie', 'Erika', 'Barton', 'Clinton', 'Greg', 'Colleen', 'Doris', 'Ramiro', 'Bonnie', 'Destiny', 'Paula', 'Preston', 'Darla', 'Jerrie', 'Francine', 'Adam', 'Rena', 'Adele', 'Tracy', 'Vivian', 'Darrell', 'Rogelio', 'Sandy', 'Britney', 'Boris', 'Miguel', 'Marian', 'Lauren', 'Rosaura', 'Megan', 'Elvia', 'Emma', 'Beverlee', 'Stephanie', 'Cherie', 'Mitchell', 'Faye', 'Dale', 'Caleb', 'Lily', 'Savannah', 'Teodoro', 'Constance', 'Duane', 'Woodrow', 'Myra', 'Eula', 'Myrtle', 'Manuel', 'Jacquelyn', 'Matilde', 'Jackie', 'Lonnie', 'Shelby', 'Cora', 'Nadia', 'Damon', 'Evelyn', 'Hui', 'Kirsten', 'Tamika', 'Anabel', 'Marci', 'Tony', 'Pauline', 'Sidney', 'Ann', 'Leon', 'Tamara', 'Selena', 'Jacinta', 'Rae', 'Annmarie', 'Shawn', 'Philip', 'Clayton', 'Virgil', 'Hortense', 'Sherman', 'Alberta', 'Vicki', 'Brenda', 'Regina', 'Eleanor', 'Mario', 'Benita', 'Jaleesa', 'Lloyd', 'Lavonne', 'Jacqueline', 'Jeanne', 'Saundra', 'Pedro', 'Elaine', 'Ricky', 'Clarence', 'Jane', 'Salome', 'Joy', 'Stanley', 'Wanda', 'Percy', 'Lester', 'Roy', 'Caren', 'Daisy', 'Peggy', 'Eunice', 'Tequila', 'Angelina', 'Leticia', 'Miranda', 'Sammy', 'Shaun', 'Rubin', 'Marshall', 'Becky', 'Marianne', 'Dexter', 'Missy', 'Tracey', 'Scott', 'Gerard', 'Juanita', 'Edmund', 'Sherry', 'Gino', 'Rick', 'Julienne', 'Maxine', 'Alma', 'Ilene', 'Georgina', 'Arnold', 'Nannette', 'Deanna', 'Minnie', 'Van', 'Lori', 'Daryl', 'Rex', 'Desiree', 'Renee', 'Ana', 'Wesley', 'Chung', 'Frederick', 'Nettie', 'Lizeth', 'Dana', 'Debra', 'Deborah', 'Esther', 'Ellie', 'Junior', 'Ulysses', 'Beth', 'Arturo', 'Nathaniel', 'Reta', 'Wiley', 'Rolando', 'Gilberto', 'Clyde', 'Edwin', 'Gerald', 'Warren', 'Sudie', 'Lynette', 'Antonio', 'Irma', 'Lajuana', 'Henrietta', 'Tia', 'Craig', 'Aubrey', 'Dustin', 'Carry', 'Sophia', 'Sybil', 'Marcus', 'Marina', 'Caitlin', 'Merilyn', 'Leona', 'Andy', 'Madaline', 'Noel', 'Christy', 'Trudie', 'Angelita', 'Sang', 'Mable', 'Ernestine', 'Monique', 'Thomasina', 'Courtney', 'Anastacia', 'Bessie', 'Gertrude', 'Lelia', 'Tanisha', 'Chun', 'June', 'Tammy', 'Raul', 'Danny', 'Rocky', 'Rebekah', 'Kristi', 'Jake', 'Irena', 'Babette', 'Laverne', 'Sean', 'Theodore', 'Guillermo', 'Kristina', 'Michel', 'Ronny', 'Dixie', 'Ramon', 'Rose', 'Daniella', 'Victor', 'Madeline', 'Carmella', 'Elwood', 'Wm', 'Trina', 'Cristina', 'Roberta', 'Julio', 'Roni', 'Mandie', 'Delia', 'Floyd', 'Dennis', 'Sydney', 'Marlene', 'Janette', 'Jerome', 'Georgia', 'Hien', 'Dianne', 'Gail', 'Ira', 'Karlene', 'Jeffrey', 'Jodi', 'Don', 'Jamar', 'Omar', 'Sherri', 'Cesar', 'Pamela', 'Carlene', 'Verna', 'Rickie', 'Josh', 'Lois', 'Araceli', 'Emil', 'Alton', 'Claire', 'Kate', 'Janie', 'Pablo', 'Lenny', 'Della', 'Laure', 'Isaac', 'Jolene', 'Merle', 'Irene', 'Bryon', 'Lewis', 'Gordon', 'Geraldine', 'Berniece', 'Leland', 'Sheree', 'Patty', 'Merrill', 'Hope', 'Genevieve', 'Stefanie', 'Ladonna', 'Travis', 'Gilda', 'Emory', 'Angeline', 'Edythe', 'Aileen', 'Francis', 'Riley', 'Vance', 'Mercedez', 'Mack', 'Fannie', 'Rosalinda', 'Jacklyn', 'Ricardo', 'Emmitt', 'Ken', 'Marla', 'Allan', 'Eloise', 'Monte', 'Zackary', 'Gena', 'Harley', 'Gwendolyn', 'Thurman', 'Sheryl', 'Vicente', 'Phillip', 'Jermaine', 'Joni', 'Rosa', 'Herman', 'Velma', 'Dianna', 'Shizuko', 'Heidi', 'Maurice', 'Marisol', 'Charity', 'Geneva', 'Amber', 'Lyn', 'Jay', 'Mae', 'Graciela', 'Delores', 'Alena', 'Charlie', 'Jeanette', 'Antonietta', 'Rhonda', 'Ivan', 'Stanton', 'Austin', 'Leola', 'Diane', 'Dalton', 'Therese', 'Tammera', 'Lidia', 'Lottie', 'Leisa', 'Marisa', 'Sanda', 'Arlene', 'Charolette', 'Burton', 'Samantha', 'Dee', 'Rona', 'Aline', 'Lou', 'Jenette', 'Marcia', 'Viola', 'Kerry', 'Debi', 'Lindsey', 'Devorah', 'Dorene', 'Lucile', 'Elsie', 'Mitzi', 'Hong', 'Terrell', 'Mariano', 'Randall', 'Sammie', 'Sophie', 'Stuart', 'Devin', 'Danial', 'Arleen', 'Randal', 'Belinda', 'Loren', 'Connie', 'Dean', 'Brain', 'Lorenzo', 'Clare', 'Alfredo', 'Alta', 'Desire', 'Wilbur', 'Arletta', 'Dante', 'Nola', 'Katie', 'Kary', 'Dorian', 'Christian', 'Alejandra', 'Phyllis', 'Darrel', 'Chandra', 'Yael', 'Brittani', 'Bennett', 'Terra', 'Jenifer', 'Sherwood', 'Lucille', 'Shanna', 'Vonda', 'Caitlyn', 'Sue', 'Bernardo', 'Imelda', 'Cathern', 'Lacresha', 'Renata', 'Landon', 'Jeremy', 'Herbert', 'Alina', 'Roseann', 'Cliff', 'Wilma', 'Delta', 'Jarrod', 'Nelson', 'Freeda', 'Jaimie', 'Shavonda', 'Danna', 'Darryl', 'Esta', 'Kellye', 'Lorena', 'Gerda', 'Filiberto', 'Dakota', 'Richie', 'Irving', 'Maura', 'Denny', 'Astrid', 'Joe', 'Yong', 'Diana', 'Roselee', 'Carlo', 'Shane', 'Dave', 'Jenni', 'Noemi', 'Doug', 'Sam', 'Ingrid', 'Audra', 'Noreen', 'Marcos', 'Aletha', 'Boyd', 'Neil', 'Dudley', 'Earnestine', 'Kristine', 'Adrian', 'Charleen', 'Tillie', 'Troy', 'Reynaldo', 'Gilbert', 'Nadine', 'Homer', 'Jovita', 'Taylor', 'Guadalupe', 'Margery', 'Micheal', 'Erma', 'Celia', 'Mathilde', 'Hannah', 'Marcella', 'Rowena', 'Tommy', 'Tommie', 'Jena', 'Sierra', 'Silvia', 'Jannie', 'Brittney', 'Eduardo', 'Betsy', 'Dwayne', 'Rodrigo', 'Murray', 'Keri', 'Opal', 'Reginald', 'Flora', 'Gabriel', 'Mina', 'Nanette', 'Dwight', 'Jeannette', 'Beryl', 'Coleman', 'Javier', 'Zina', 'Santos', 'Latoya', 'Gwen', 'Antionette', 'Hugo', 'Tricia', 'Aurora', 'Cassie', 'Ginny', 'Johnna', 'Vera', 'Rosie', 'Carlotta', 'Arlen', 'Angie', 'Lilly', 'Buford', 'Nestor', 'Delmar', 'Gala', 'Demetria', 'Josefina', 'Armando', 'Lowell', 'Freddy', 'Alexandra', 'Rudolph', 'Winnie', 'Etta', 'Wilbert', 'Rudolf', 'Cristin', 'Drew', 'Nora', 'Christie', 'Joella', 'Tammi', 'Donte', 'Marsha', 'Valeria', 'Brianne', 'Meaghan', 'Marketta', 'Corie', 'Marx', 'Adolfo', 'Corrine', 'Ella', 'Joellen', 'Harriett', 'Dann', 'Rufus', 'Annetta', 'Ericka', 'Cara', 'Candace', 'Karla', 'Laurene', 'Shari', 'France', 'Ahmad', 'Clementina', 'Dick', 'Alison', 'Carole', 'Brett', 'Zachary', 'Darren', 'Melodie', 'Mamie', 'Allyson', 'Grant', 'Meghan', 'Cherry', 'Stella', 'Sallie', 'Avis', 'Brooks', 'Paulette', 'Cari', 'Vennie', 'Jeremiah', 'Kellie', 'Alisa', 'Yvette', 'Melody', 'Merlin', 'Josue', 'Elisabeth', 'Kristin', 'Toby', 'Lakeshia', 'Donnell', 'Irvin', 'Elda', 'Lanny', 'Norine', 'Roseline', 'Parthenia', 'Antonia', 'Coleen', 'Marybelle', 'Gerry', 'Goldie', 'Vikki', 'Corey', 'Cleveland', 'Johnathon', 'Calvin', 'Jana', 'Adolph', 'Roscoe', 'Chong', 'Hank', 'Damion', 'Alda', 'Mai', 'Andreas', 'Jo', 'Nedra', 'Pearl', 'Celeste', 'Delma', 'Franklin', 'Dreama', 'Effie', 'Wendell', 'Bernie', 'Johanna', 'Milissa', 'Salvador', 'Rosanna', 'Alesia', 'Naomi', 'Robyn', 'Benjamin', 'Conrad', 'Stephine', 'Ellis', 'Bert', 'Seth', 'Lynda', 'Brigette', 'Kathrine', 'Christa', 'Quinton', 'Marvel', 'Carmon', 'Lura', 'Dewey', 'Perry', 'Vernon', 'Refugio', 'Stan', 'Jennie', 'Sonia', 'Elnora', 'Joelle', 'Traci', 'Kristie', 'Jame', 'Trevor', 'Selene', 'Phil', 'Edmundo', 'Ginger', 'Lonna', 'Eugenia', 'Hillary', 'Hildred', 'Emmie', 'Rosy', 'Moses', 'Dena', 'Ivette', 'Stacey', 'Jina', 'Guillermina', 'Reggie', 'Josette', 'Isaura', 'Blanche', 'Cary', 'Carolina', 'Maritza', 'Enrique', 'Frankie', 'Norbert', 'Ramona', 'Evalyn', 'Mason', 'Darius', 'Millard', 'Jude', 'Cody', 'Lourdes', 'Emerson', 'Lydia', 'Arron', 'Tarsha', 'Tessie', 'Young', 'Kelli', 'Bettie', 'Lesley', 'Rita', 'Walton', 'Elliott', 'Kanisha', 'Bridget', 'Kirk', 'Alejandro', 'Nina', 'Jenna', 'Sal', 'Blake', 'Patrice', 'Vickey', 'Chet', 'Dara', 'Joey', 'Neal', 'Noelle', 'Zula', 'Dewitt', 'Alonzo', 'Martina', 'Lorene', 'Hector', 'Gayle', 'Tammie', 'Emanuel', 'Bernadette', 'Pansy', 'Heriberto', 'Tomas', 'Heath', 'Amelia', 'Brandie', 'Olga', 'Marc', 'Tabitha', 'Trent', 'Kristy', 'Jan', 'Tiffiny', 'Toni', 'Charlene', 'Rene', 'Morton', 'Hattie', 'Ok', 'Lakia', 'Taryn', 'Ward', 'Tracie', 'Millie', 'Karin', 'Bethann', 'Shelia', 'Fernando', 'Alethea', 'Clifford', 'Sunday', 'Bradly', 'Jodie', 'Noelia', 'Rosalyn', 'Tanya', 'Marguerite', 'Deon', 'Elois', 'Lillie', 'Augusta', 'India', 'Johnathan', 'Keisha', 'Lyla', 'Kip', 'Rashida', 'Mimi', 'Margarita', 'Estella', 'Tristan', 'Justa', 'Melinda', 'Ebony', 'Susie', 'Harland', 'Markus', 'Erwin', 'Larhonda', 'Archie', 'Roselle', 'Nydia', 'Patsy', 'Shantel', 'Lue', 'Idell', 'Junko', 'Grace', 'Humberto', 'Genoveva', 'Fawn', 'Rod', 'Kristopher', 'Wes', 'Pete', 'Toya', 'Jed', 'Jaqueline', 'Windy', 'Ernesto', 'Lula', 'Ivory', 'Yolande', 'Petra', 'Gearldine', 'Isabel', 'Lilian', 'Ava', 'Flossie', 'Russ', 'Beatriz', 'Hilaria', 'Cristopher', 'Jared', 'Otis', 'Louella', 'Kara', 'Rosetta', 'Rosalie', 'Roxanne', 'Joaquin', 'Tomasa', 'Teofila', 'Mel', 'Socorro', 'Jim', 'Jerald', 'Devon', 'Shellie', 'Felix', 'Mervin', 'Agnes', 'Salvatore', 'Mara', 'Otto', 'Rhea', 'Jackeline', 'Kendrick', 'Brendan', 'Wilton', 'Harvey', 'Cecelia', 'Eddy', 'Britt', 'Myrna', 'Zachery', 'Twila', 'Angelo', 'Cornelius', 'Katharina', 'Jasmine', 'Aurelio', 'Jefferson', 'Lyle', 'Tami', 'Carri', 'Marisela', 'Katrina', 'Werner', 'Ashlee', 'Zack', 'Norman', 'Elaina', 'Jacques', 'Kandace', 'Shanta', 'Leesa', 'Alyce', 'Vernice', 'Sharyl', 'Erik', 'Dollie', 'Myrtis', 'Glynda', 'Nakia', 'Rocco', 'Lora', 'Rudy', 'Kurt', 'Nichole', 'Christi', 'Silas', 'Jesusa', 'Jacinto', 'Rosalind', 'Justina', 'Dominick', 'Leah', 'Ronda', 'Ed', 'Teresita', 'Marna', 'Solomon', 'Jarrett', 'Fonda', 'Hugh', 'Robby', 'Cecilia', 'Lakesha', 'Leora', 'Rhoda', 'Darin', 'Dewayne', 'Janis', 'Benito', 'Gale', 'Willard', 'Rodolfo', 'Charla', 'Emery', 'Timmy', 'Anton', 'Pamala', 'Bettye', 'Zelma', 'Migdalia', 'Owen', 'Ron', 'Stevie', 'Vaughn', 'Arden', 'Maudie', 'Tashia', 'Roslyn', 'Stacie', 'Abbie', 'Donny', 'Rachelle', 'Jenine', 'Alesha', 'Trey', 'Jeni', 'Dusty', 'Mauro', 'Polly', 'Edie', 'Oscar', 'Gretchen', 'Ferdinand', 'Edgardo', 'Erick', 'Byron', 'Cruz', 'Arlinda', 'In', 'Meredith', 'Daniele', 'Brooke', 'Awilda', 'Lin', 'Lazaro', 'Billie', 'Estela', 'Willis', 'Luz', 'Deloris', 'Sima', 'Matt', 'Sheri', 'Larue', 'Sarina', 'Lola', 'Tomiko', 'Ruben', 'Kari', 'Fern', 'Staci', 'Aimee', 'Whitney', 'Fidel', 'Oliver', 'Colene', 'Nona', 'Federico', 'Colin', 'Fabian', 'Gabrielle', 'Caryn', 'Reba', 'Nery', 'Fredrick', 'Lindy', 'Roland', 'Morris', 'Ethan', 'Freeman', 'Elisa', 'Von', 'Lezlie', 'Debby', 'Nita', 'Maggie', 'Lara', 'Danelle', 'Retha', 'Danilo', 'Jewell', 'Jennette', 'Deane', 'Mohammed', 'Quinn', 'Quentin', 'Linwood', 'Chasity', 'Karon', 'Marietta', 'Christin', 'Deirdre', 'Newton', 'Fran', 'Jefferey', 'Freddie', 'Marcel', 'Marco', 'Kaitlin', 'Denita', 'Tasha', 'Dora', 'Eldridge', 'Dani', 'Elsa', 'Maricela', 'Carrol', 'Quincy', 'Carolynn', 'Consuelo', 'Lakeisha', 'Stewart', 'Bruno', 'Clint', 'Kiesha', 'Iva', 'Mona', 'Lucrecia', 'Myron', 'Gussie', 'Sonya', 'Gladis', 'Deidra', 'Alana', 'Donnie', 'Charisse', 'Sandi', 'Marlys', 'Matilda', 'Sadie', 'Ardell', 'Max', 'Maryanne', 'Kathyrn', 'Sabrina', 'Minh', 'Greta', 'Dorcas', 'Tonia', 'Evangeline', 'Lona', 'Margrett', 'Romeo', 'Daphne', 'Odell', 'Horacio', 'Emmett', 'Amie', 'August', 'Elbert', 'Gabriela', 'Cinthia', 'Armand', 'Julianne', 'Beverley', 'Lessie', 'Ina', 'Mayme', 'Lolita', 'Lyndsay', 'Marcelino', 'Leatrice', 'Marcellus', 'Jarred', 'Kasey', 'Merry', 'Elena', 'Kindra', 'Jarvis', 'Bethel', 'Else', 'Kathi', 'Dotty', 'Xiomara', 'Latoria', 'Juliana', 'Len', 'Lacey', 'Debora', 'Serena', 'Reuben', 'Hilton', 'Luann', 'Nickolas', 'Emilia', 'Amberly', 'Bertram', 'Cori', 'Alisha', 'Helene', 'Virgie', 'Octavio', 'Millicent', 'Prince', 'Janna', 'Shelli', 'Chrystal', 'Domonique', 'Candida', 'Rob', 'Wilhelmina', 'Eveline', 'Carlton', 'Shameka', 'Paige', 'Vicky', 'Saul', 'Shirlene', 'Mirna', 'Mellisa', 'Danuta', 'Ambrose', 'Lang', 'Nolan', 'Geoffrey', 'Ty', 'Michaela', 'Dorthy', 'Camelia', 'Clark', 'Melynda', 'Ilse', 'Garnet', 'Laureen', 'Bud', 'Valarie', 'Karrie', 'Jamison', 'Raphael', 'Benedict', 'Senaida', 'Briana', 'Vada', 'Casey', 'Angelia', 'Cyrus', 'Gustavo', 'Denis', 'Asha', 'Walker', 'Tiffaney', 'Mandy', 'Earline', 'Neville', 'Clementine', 'Abigail', 'Lyda', 'Jamal', 'Tempie', 'Camille', 'Angelica', 'Amalia', 'Christen', 'Wallace', 'Leann', 'Patti', 'Belle', 'Marty', 'Tamisha', 'Noah', 'Annemarie', 'Colton', 'Jazmin', 'Jada', 'Earle', 'Maud', 'Ruthie', 'Felipe', 'Clora', 'Lashon', 'Jenell', 'Aretha', 'Violet', 'Candice', 'Lizzie', 'Arcelia', 'Cathryn', 'Karol', 'Ted', 'Earnest', 'Debrah', 'Alden', 'Lissa', 'Aleta', 'Remedios', 'Tobias', 'Vella', 'Celina', 'Simon', 'Blanch', 'Mirella', 'Abby', 'Kenny', 'Lon', 'Jessenia', 'Charley', 'Ned', 'Felecia', 'Blair', 'Samatha', 'Leslee', 'Kareem', 'Susanne', 'Alba', 'Zulema', 'Arline', 'Jenniffer', 'Esperanza', 'Santiago', 'Iona', 'Brendon', 'Mariah', 'Doreen', 'Alejandrina', 'Adrianne', 'Teressa', 'Sharron', 'Marcela', 'Errol', 'Cleo', 'Jannette', 'Rosalee', 'Sonja', 'Art', 'Debroah', 'Caterina', 'Jeanine', 'Chanel', 'Melisa', 'Yoko', 'Romana', 'Ofelia', 'Carmelita', 'Gaston', 'Reed', 'Darron', 'Concepcion', 'Sherly', 'Mickey', 'Cameron', 'Addie', 'Thanh', 'Candy', 'Celestine', 'Lavonia', 'Adeline', 'Ezra', 'Ardis', 'Ike', 'Alycia', 'Fay', 'Margo', 'Imogene', 'Lakisha', 'Luisa', 'Zelda', 'Brigid', 'Lucia', 'Latesha', 'Fatima', 'Dawne', 'Dorris', 'Sunshine', 'Zenaida', 'Kylee', 'Jeffry', 'Jayne', 'Idalia', 'Bart', 'Tawnya', 'Crissy', 'Alline', 'Gracie', 'Melonie', 'Dorethea', 'Sibyl', 'Nelda', 'Shelley', 'Hubert', 'Dagmar', 'Carroll', 'Harrison', 'Nan', 'Argelia', 'Rusty', 'Sherlyn', 'Juli', 'Kermit', 'Nickie', 'Leila', 'Vania', 'Helena', 'Sherie', 'Mercedes', 'Elias', 'Alva', 'Hollis', 'Milo', 'Roseanna', 'Geraldo', 'Malka', 'Grover', 'Josef', 'Sol', 'Evelia', 'Jenelle', 'Burt', 'Rochelle', 'Maxima', 'Jocelyn', 'Vida', 'Jeri', 'Kandy', 'Jasmin', 'Estelle', 'Caridad', 'Gaynelle', 'Vito', 'Sigrid', 'Victorina', 'Latasha', 'Nicola', 'Edmond', 'Omer', 'Carey', 'Mia', 'Lennie', 'Charmaine', 'Wendi', 'Brianna', 'Lawerence', 'Erich', 'Erline', 'Aurelia', 'Zoraida', 'Myriam', 'Rory', 'Concetta', 'Sulema', 'Johnie', 'Adela', 'Felipa', 'Yadira', 'Israel', 'Ophelia', 'Zella', 'Noella', 'Maurine', 'Jarod', 'Georgette', 'Derick', 'Alfonso', 'Elfriede', 'Brigitte', 'Raymundo', 'Reid', 'Enriqueta', 'Valentina', 'Octavia', 'Shelly', 'Jackson', 'Lavina', 'Maisie', 'Bea', 'Risa', 'Priscilla', 'Scotty', 'Vanesa', 'Jillian', 'Mee', 'Carina', 'Liza', 'Keshia', 'Teri', 'Kitty', 'Dorthea', 'Brandy', 'Marlin', 'Oma', 'Maude', 'Lavinia', 'Gricelda', 'Brenton', 'Chloe', 'Minerva', 'Cherly', 'Kristyn', 'Keena', 'Alecia', 'Scottie', 'Herschel', 'Isaiah', 'Vicenta', 'Fe', 'Dorothea', 'Tanja', 'Palma', 'Elijah', 'Ervin', 'Krista', 'Ela', 'Leta', 'Osvaldo', 'Jacquelin', 'Anderson', 'Vivien', 'Truman', 'Ricarda', 'Wilford', 'Madge', 'Kenton', 'Garrett', 'Cole', 'Stefan', 'Kathey', 'Micaela', 'Nicolas', 'Hilario', 'Sofia', 'Judi', 'Corine', 'Reva', 'Hassan', 'Ismael', 'Nathanael', 'Bulah', 'Marilee', 'Wilburn', 'Margot', 'Anneliese', 'Mollie', 'Yuk', 'Veda', 'Russel', 'Luciano', 'Myles', 'Yesenia', 'Juliette', 'Perla', 'Cleta', 'Iliana', 'Telma', 'Roosevelt', 'Daphine', 'Pattie', 'Carter', 'Freda', 'Mariel', 'Nakesha', 'Lamont', 'Ora', 'Aldo', 'Pricilla', 'Avelina', 'German', 'Zane', 'Jolie', 'Amiee', 'Isabelle', 'Dayna', 'Mindy', 'Leisha', 'Germaine', 'Savanna', 'Luke', 'Agustin', 'Lana', 'Anya', 'Yasmine', 'Laurence', 'Cleopatra', 'Genaro', 'Suzette', 'Jeanie', 'Margarete', 'Josie', 'Grady', 'Athena', 'Frederic', 'Maybell', 'Glenna', 'Johnetta', 'Ola', 'Lorna', 'Booker', 'Jamila', 'Racheal', 'Bess', 'Deana', 'Evon', 'Donya', 'Raven', 'Randolph', 'Bonita', 'Elvira', 'Cleora', 'Winfred', 'Sherrie', 'Vanna', 'Lorrie', 'Jae', 'Reiko', 'Hang', 'Lucinda', 'Desmond', 'Laraine', 'Georgine', 'Dominique', 'Luna', 'Holli', 'Julius', 'Marquita', 'Chantelle', 'Deandre', 'Alyssa', 'Wilfred', 'Eulalia', 'Ulrike', 'Maxwell', 'Karey', 'Randi', 'Michiko', 'Shonda', 'Verda', 'Kathaleen', 'Forrest', 'Randa', 'Delphine', 'Augustine', 'Enoch', 'Janita', 'Janell', 'Kirby', 'Lenna', 'Brunilda', 'Flor', 'Zoila', 'Suzanna', 'Coy', 'Bridgette', 'Beatris', 'Winston', 'Leonora', 'Lenora', 'Eufemia', 'Darcy', 'Erasmo', 'Svetlana', 'Williemae', 'Maryjane', 'Leanna', 'Ena', 'Inga', 'Hortencia', 'Norris', 'Phylis', 'Ellyn', 'Wade', 'Ula', 'Roman', 'Benny', 'Dirk', 'Deena', 'Bryce', 'Harlan', 'Freida', 'Deann', 'Emelina', 'Arnita', 'Sonny', 'Lizette', 'Treasa', 'Iesha', 'Lenore', 'Bula', 'Loyd', 'Elton', 'Jeannie', 'Nilda', 'Irmgard', 'Antoine', 'Phillis', 'Nikita', 'Shira', 'Lala', 'Cordelia', 'Kathie', 'Stephan', 'Al', 'Tesha', 'Toney', 'Natasha', 'Michal', 'Rosario', 'Zaida', 'Jolynn', 'Joeann', 'Margarette', 'Odette', 'Racquel', 'Dona', 'Hester', 'Reina', 'Shon', 'Hal', 'Laurette', 'Alix', 'Marylou', 'Trudy', 'Faith', 'Kendra', 'Stacee', 'Jewel', 'Ivana', 'Lavada', 'Sheldon', 'Vernell', 'Marlena', 'Numbers', 'Maribel', 'Georgie', 'Janetta', 'Ashely', 'Thresa', 'Neva', 'Cyril', 'Thuy', 'Deanne', 'Peggie', 'Robbie', 'Monika', 'Bennie', 'Roselyn', 'Donovan', 'Vernia', 'Susann', 'Sid', 'Rosalia', 'Hung', 'Isaias', 'Olive', 'Abel', 'Tierra', 'Tameka', 'Jerri', 'Nada', 'Lyndsey', 'Mellissa', 'Cyndi', 'Denice', 'Annabel', 'Meagan', 'Efren', 'Bobbi', 'Pilar', 'Lupita', 'Siu', 'Casandra', 'Rosendo', 'Norberto', 'Alanna', 'Katelyn', 'Clarissa', 'Earlean', 'Alfreda', 'Merlene', 'Nicolette', 'Sasha', 'Elia', 'Carola', 'Shanika', 'Louann', 'Colette', 'Rafaela', 'Chance', 'Mariette', 'Lisha', 'Elma', 'King', 'Cami', 'Claudine', 'Gemma', 'Wilson', 'Janelle', 'Alia', 'Delpha', 'Ami', 'Antonette', 'Glendora', 'Diego', 'Dominque', 'Lucas', 'Crista', 'Daren', 'Margret', 'Luba', 'Katy', 'Natividad', 'Sondra', 'Carley', 'Elizbeth', 'Hiram', 'Andra', 'Arielle', 'Dinah', 'Viviana', 'Laticia', 'Kristan', 'Leigha', 'Florene', 'Avery', 'Mitchel', 'Melva', 'Ming', 'Silva', 'Delmer', 'Dalene', 'Anja', 'Jacque', 'Autumn', 'Rosamond', 'Chelsea', 'Collin', 'Aurore', 'Hollie', 'Kris', 'Jamey', 'Dolly', 'Marva', 'Ryann', 'Ross', 'Zachariah', 'Tiana', 'Kina', 'Shante', 'Tyson', 'Renea', 'Sherryl', 'Annice', 'Dalia', 'Del', 'Waldo', 'Bertie', 'Kandi', 'Krystyna', 'Concha', 'Ileana', 'Esteban', 'Kenya', 'Carolee', 'Jeneva', 'Eugenie', 'Leeann', 'Jacqualine', 'Claudette', 'Rhiannon', 'Ernie', 'Sharolyn', 'Sina', 'Armandina', 'Gus', 'Lacy', 'Brinda', 'Fernanda', 'Hayley', 'Galina', 'Darrin', 'Susanna', 'Kathlyn', 'Tressie', 'Sung', 'Ahmed', 'Margarito', 'Margorie', 'Mira', 'Margarett', 'Cheyenne', 'Contessa', 'Liberty', 'Stacia', 'Kimberlie', 'Stephania', 'Bette', 'Lucretia', 'Emilio', 'Miles', 'Cathleen', 'Evonne', 'Ivy', 'Curt', 'Tessa', 'An', 'Katina', 'Rickey', 'Logan', 'Angele', 'Wally', 'Dina', 'Shu', 'Hortensia', 'Lili', 'Melvina', 'Leota', 'Winona', 'Leif', 'Candance', 'Janene', 'Jami', 'Naoma', 'Jonnie', 'Willa', 'Camilla', 'Bettyann', 'Milly', 'Vince', 'Roxane', 'Louie', 'Delilah', 'Rosita', 'Jospeh', 'Tyron', 'Jeane', 'Herlinda', 'Claudio', 'Consuela', 'Alexandria', 'Florine', 'Elinore', 'Lekisha', 'Dannie', 'Carmelo', 'Nell', 'Nathalie', 'Eustolia', 'Maximina', 'Regena', 'Shaunna', 'Leone', 'Lore', 'Emogene', 'Mariann', 'Elsy', 'Alfonzo', 'Everette', 'Madeleine', 'Amos', 'Dawna', 'Libby', 'Penelope', 'Liz', 'Cyndy', 'Frieda', 'Emerita', 'Susannah', 'Adelaida', 'Fallon', 'Kiara', 'Odis', 'Beata', 'Dominic', 'Marianna', 'Celena', 'Sharee', 'Twyla', 'Rosella', 'Kimberley', 'Charlyn', 'Cortney', 'Gertie', 'Kristofer', 'Iola', 'Jasper', 'Krystle', 'Margert', 'Clay', 'Thaddeus', 'Princess', 'Darci', 'Gay', 'Madison', 'Donn', 'Wilfredo', 'Gregorio', 'Giovanna', 'Kimi', 'Britni', 'Zoe', 'Inocencia', 'Luella', 'Louanne', 'Leonor', 'Deidre', 'Antony', 'Dottie', 'Mac', 'Leonel', 'Rosalina', 'Valentin', 'Alphonso', 'Stefany', 'Lavern', 'Marybeth', 'Tamra', 'Rosette', 'Annis', 'Precious', 'Thersa', 'Pierre', 'Barbra', 'Les', 'Breann', 'Mckinley', 'Trish', 'Katharyn', 'Jerrold', 'Neoma', 'Jonas', 'Illa', 'Sheridan', 'Fletcher', 'Starla', 'Ayako', 'Moira', 'Enola', 'Aida', 'Tonda', 'Edwina', 'Evangelina', 'Miguelina', 'Mariana', 'Vesta', 'Jesica', 'Mirta', 'Sachiko', 'Nakita', 'Kym', 'Kizzy', 'Hans', 'Elroy', 'Dulce', 'Demarcus', 'Samara', 'Jenice', 'Catina', 'Elease', 'Madelyn', 'Gavin', 'Jeramy', 'Latanya', 'Evie', 'Shanti', 'Emilie', 'Ima', 'Londa', 'Nanci', 'Simone', 'Alysia', 'Alida', 'Melda', 'Apryl', 'Hettie', 'Kiley', 'Isidro', 'Mayra', 'Paulita', 'Williams', 'Fredric', 'Lamar', 'Kassandra', 'Ali', 'Bonny', 'Velia', 'Waneta', 'Lynetta', 'Damian', 'Royal', 'Bridgett', 'Versie', 'Maryetta', 'Nevada', 'Tresa', 'Pearlene', 'Cathie', 'Jonna', 'Exie', 'Seymour', 'Eloisa', 'Alexa', 'Tomeka', 'Josefa', 'Oralee', 'Arla', 'Alvina', 'Marisha', 'Sarita', 'Francisca', 'Oliva', 'Hyacinth', 'Aja', 'Masako', 'Vonnie', 'Vertie', 'Karoline', 'Maya', 'Chang', 'Corliss', 'Jenee', 'Eda', 'Delphia', 'January', 'Geri', 'Alissa', 'Buffy', 'Letha', 'Chiquita', 'Malinda', 'Breanna', 'Allene', 'Garret', 'Nannie', 'Coletta', 'Lina', 'Helga', 'Larissa', 'Daron', 'Tania', 'Ellan', 'Melissia', 'Cornell', 'Eloy', 'Luciana', 'Josephina', 'Joya', 'Lenard', 'Jeanice', 'Delinda', 'Tamela', 'Tawanna', 'Shanon', 'Lauran', 'Fidelia', 'Royce', 'Sharika', 'Librada', 'Delbert', 'Latosha', 'Elida', 'Flo', 'Alla', 'Gregoria', 'Bettina', 'Hailey', 'Ewa', 'Jeanna', 'Isiah', 'Kelsey', 'Tawna', 'Barbar', 'Chuck', 'Abram', 'Herminia', 'Efrain', 'Suzan', 'Lisabeth', 'Ardelle', 'Liliana', 'Jeannine', 'Beau', 'Rosalba', 'Deb', 'Kerstin', 'Yolando', 'Nathanial', 'Gilberte', 'Marcy', 'Latonya', 'Amada', 'Bret', 'Carman', 'Tanesha', 'Lanie', 'Granville', 'Margit', 'Dionne', 'Marilynn', 'Hyman', 'Raylene', 'Magdalene', 'Rigoberto', 'Eugenio', 'Dominica', 'Emile', 'Danika', 'Signe', 'Kristal', 'Keely', 'Edwardo', 'Erlinda', 'Khadijah', 'Ursula', 'Lashonda', 'Wilda', 'Angla', 'Vincenzo', 'Carline', 'Alyson', 'Michaele', 'Liana', 'Sterling', 'Cassi', 'Brice', 'Reyna', 'Elke', 'Shea', 'Willena', 'Letty', 'Gil', 'Marjory', 'Aisha', 'Florrie', 'Marquis', 'Tana', 'Lisette', 'Hobert', 'Christiane', 'Laurel', 'Rico', 'Mica', 'Chastity', 'Santa', 'Hilary', 'Lupe', 'Malvina', 'Alvera', 'Jodee', 'Casie', 'Haywood', 'Carissa', 'Leeanna', 'Harris', 'Nisha', 'Hedy', 'Catherin', 'Sherley', 'Leopoldo', 'Gaye', 'Nidia', 'Leilani', 'Mandi', 'Mavis', 'Otha', 'Melina', 'Nelle', 'Burl', 'Tory', 'Paris', 'Margurite', 'Clemente', 'Louisa', 'Cathey', 'Corinne', 'Lyndon', 'Hye', 'Alease', 'Loan', 'Eryn', 'Lauretta', 'Genna', 'Karissa', 'Nichol', 'Marta', 'Angelika', 'Griselda', 'Jordon', 'Kaitlyn', 'Letitia', 'Karina', 'Norah', 'Lise', 'Maren', 'Georgiann', 'Jazmine', 'Sha', 'Cherise', 'Lane', 'Shayna', 'Maryellen', 'Shakia', 'Queen', 'Ligia', 'Bianca', 'Delora', 'Emmanuel', 'Raymon', 'Kieth', 'Philomena', 'Katlyn', 'Doretha', 'Mckenzie', 'Mauricio', 'Denver', 'Susana', 'Juliann', 'Trena', 'Marchelle', 'Eldon', 'Klara', 'Natalia', 'Tyree', 'Pandora', 'Sharyn', 'Adaline', 'Anika', 'Elmo', 'Diamond', 'Lashaunda', 'Pauletta', 'Jacki', 'Rhona', 'Lino', 'Blaine', 'Parker', 'Chantel', 'Lurline', 'Shad', 'Kandice', 'Alita', 'Kimberlee', 'Phuong', 'Laci', 'Kesha', 'Cicely', 'Palmira', 'Fidela', 'Delois', 'Myrtie', 'Lea', 'So', 'Cythia', 'Gerri', 'Tobi', 'Renato', 'Gudrun', 'Meri', 'Eugena', 'Pennie', 'Olen', 'Zora', 'Cindi', 'Rubye', 'Barbie', 'Wanita', 'Angelique', 'Altha', 'Elna', 'Elmira', 'Malika', 'Linette', 'Arnulfo', 'Amparo', 'Mari', 'Adan', 'Davina', 'Dorinda', 'Irwin', 'Tamiko', 'Richelle', 'Mohammad', 'Brandee', 'Annamae', 'Sabra', 'Kimberely', 'Rueben', 'Kenisha', 'Lurlene', 'Judson', 'Hunter', 'Mittie', 'Robt', 'Kathe', 'Cherilyn', 'Kati', 'Nieves', 'Oren', 'Kori', 'Dell', 'Carson', 'Tisha', 'Jonelle', 'Jonah', 'Shery', 'Monty', 'Loni', 'Oralia', 'Theresia', 'Allie', 'Theodora', 'Ozell', 'Sanford', 'Janyce', 'Jayme', 'Kisha', 'Elin', 'Phung', 'Rodrick', 'Jacalyn', 'Hosea', 'Myong', 'Trudi', 'Jerrod', 'Xavier', 'Gayla', 'Dessie', 'Majorie', 'Dyan', 'Katheryn', 'Evelina', 'Twanna', 'Korey', 'Mohamed', 'Tenisha', 'Linnie', 'Tamera', 'Floy', 'Elliot', 'Kaye', 'Talisha', 'Chin', 'Soledad', 'Earlene', 'Zona', 'Demetrius', 'Latisha', 'Karie', 'Carmela', 'Treva', 'Sheba', 'Nicol', 'Layla', 'Tori', 'Adelaide', 'Robbin', 'Kaley', 'Long', 'Bunny', 'Giovanni', 'Henriette', 'Kandis', 'Vanita', 'Ermelinda', 'Sherrill', 'Kerrie', 'Shakira', 'Penney', 'Shona', 'Cecila', 'Loralee', 'Cira', 'Bernadine', 'Felton', 'Latia', 'Bernita', 'Estefana', 'Keira', 'Modesta', 'Garfield', 'Anh', 'Katharine', 'Siobhan', 'Marinda', 'Jc', 'Lacie', 'Ramonita', 'Vilma', 'Val', 'Audry', 'Albertina', 'Hana', 'Cinda', 'Tera', 'Tanna', 'Magdalena', 'Keiko', 'Anjelica', 'Elise', 'Sharla', 'Janay', 'Janine', 'Reyes', 'Carmel', 'Kyla', 'Birdie', 'Velda', 'Krysta', 'Venus', 'Bibi', 'Renaldo', 'Ema', 'Scot', 'Cordell', 'Nova', 'Francie', 'Anastasia', 'Phoebe', 'Dori', 'Lynell', 'Marquetta', 'Emmy', 'Shae', 'Hoa', 'Mireya', 'Pei', 'Adella', 'Teddy', 'Inge', 'Easter', 'Trinidad', 'Novella', 'Clemencia', 'Leonore', 'Nga', 'Domenic', 'Sheena', 'Seema', 'Natisha', 'Annabell', 'Paulina', 'Janel', 'Kellee', 'Rayford', 'Nicky', 'Jaye', 'Sharilyn', 'Madie', 'Paola', 'Cortez', 'Rosanne', 'Keenan', 'Milagro', 'Ginette', 'Nereida', 'Marget', 'Corina', 'Jeanelle', 'Rebeca', 'Darleen', 'Kassie', 'Rocio', 'Elanor', 'Layne', 'Hayden', 'Joana', 'Bella', 'Eilene', 'Renay', 'Oswaldo', 'Lulu', 'Georgiana', 'Columbus', 'Karan', 'Florida', 'Daisey', 'Sabine', 'Miyoko', 'Lynnette', 'Keven', 'Annalisa', 'Detra', 'Harriette', 'Necole', 'Reda', 'Venessa', 'Johnson', 'Meggan', 'Kristeen', 'Anibal', 'Patience', 'Jessika', 'Aleen', 'Vina', 'Theo', 'Kasie', 'Zita', 'Lavenia', 'Felicitas', 'Quintin', 'Kacie', 'Deneen', 'Trisha', 'Corrie', 'Cedrick', 'Moshe', 'Sharlene', 'Rosaline', 'Marlyn', 'Diann', 'Arlena', 'Soraya', 'Ronni', 'Anissa', 'Danica', 'Ghislaine', 'Ernestina', 'Carie', 'Eleonora', 'Elfrieda', 'Lovetta', 'Ione', 'Kory', 'Buddy', 'Wilber', 'Foster', 'Dania', 'Stefania', 'Garland', 'Elouise', 'Orpha', 'Carmelina', 'Macy', 'Palmer', 'Kira', 'Trenton', 'Shayne', 'Ka', 'Joanie', 'Suellen', 'Duncan', 'Lorita', 'Kurtis', 'Elana', 'Mallie', 'Sanjuana', 'Dwain', 'Elba', 'Fausto', 'Afton', 'Sharell', 'Danita', 'Samual', 'Wonda', 'Alise', 'Raina', 'Laverna', 'Delcie', 'Ariel', 'Asia', 'Vashti', 'Youlanda', 'Normand', 'Vivienne', 'Annamarie', 'Yanira', 'Eden', 'Tuan', 'Odessa', 'Hilma', 'Chas', 'Ingeborg', 'Vern', 'Ona', 'Thu', 'Ladawn', 'Denisha', 'Laurine', 'Josphine', 'Bell', 'Enid', 'Elenora', 'Ilona', 'Skye', 'Myrtice', 'Dominga', 'Garth', 'Patria', 'Julee', 'Claretha', 'Audrea', 'Basil', 'Kayleen', 'Marin', 'Linnea', 'Ilana', 'Adena', 'Tijuana', 'Ninfa', 'Leonardo', 'Love', 'Yun', 'Noe', 'Lesha', 'Nikole', 'Yan', 'Waltraud', 'Golden', 'Corene', 'Ruthe', 'Verla', 'Tosha', 'Floria', 'Claretta', 'Charlena', 'Selina', 'Ariane', 'Kia', 'Angelena', 'Daniela', 'Bethany', 'Chelsie', 'Giuseppe', 'Lorenza', 'Muoi', 'Shaniqua', 'Sheryll', 'Johna', 'Ma', 'Roxana', 'Lorri', 'Malia', 'Teena', 'Debera', 'Vena', 'Erna', 'Rosana', 'Chauncey', 'Darwin', 'Shaina', 'Suanne', 'Lorriane', 'Berta', 'Lorette', 'Eve', 'Tawny', 'Monet', 'Damaris', 'Jutta', 'Ruthann', 'Milagros', 'Eleanore', 'Latonia', 'Alene', 'Gillian', 'Rhett', 'Makeda', 'Fumiko', 'Hulda', 'Danette', 'Loreen', 'Aleisha', 'Arnoldo', 'Lonny', 'Lida', 'Jeana', 'Denna', 'Gaylord', 'Kenna', 'Rosalva', 'Rachal', 'Micah', 'Alvaro', 'Nerissa', 'Pamula', 'Sindy', 'Vernita', 'Isabella', 'Jenise', 'Madalyn', 'Tena', 'Blythe', 'Hermina', 'Shirleen', 'Adelina', 'Tenesha', 'Weston', 'Devona', 'Oda', 'Ouida', 'Camie', 'Eliseo', 'Yolonda', 'Shanell', 'Galen', 'Rochel', 'Venita', 'Cristi', 'Fanny', 'Cleotilde', 'Veola', 'Zena', 'Deeanna', 'Sanora', 'Phyliss', 'Mozelle', 'Fermin', 'Janae', 'Donetta', 'Julieta', 'Warner', 'Catalina', 'Loris', 'Marcelle', 'Deedra', 'Cornelia', 'Fritz', 'Antione', 'Chery', 'Loraine', 'Eusebio', 'Eleonor', 'Rich', 'Latoyia', 'Lani', 'Leatha', 'Kyung', 'Nilsa', 'Despina', 'Florencio', 'Chi', 'Olene', 'Felisha', 'Ellsworth', 'Tyra', 'Lucie', 'Mirian', 'Ashleigh', 'Leandro', 'Ayana', 'Cheryle', 'Kam', 'Wendie', 'Zandra', 'Terese', 'Sebrina', 'Niki', 'Mora', 'Sun', 'Violeta', 'Rossana', 'Cassondra', 'Jeanmarie', 'Elissa', 'Beaulah', 'Inell', 'Blossom', 'My', 'Carleen', 'Delmy', 'Carolann', 'Ines', 'Lucio', 'Cecille', 'Fredda', 'Michale', 'Maranda', 'Marti', 'Ronna', 'Pura', 'Issac', 'Idella', 'Mallory', 'Shirly', 'Lissette', 'Dion', 'Caryl', 'Ciara', 'Rosenda', 'Elizebeth', 'Alyse', 'Shiela', 'Valentine', 'Elidia', 'Elvis', 'Estell', 'Edison', 'Eleanora', 'Lucius', 'Maryjo', 'Verena', 'Ranee', 'Lashawnda', 'Francesca', 'Noriko', 'Rolanda', 'Lincoln', 'Candyce', 'Raguel', 'Rosamaria', 'Lesa', 'Nohemi', 'Filomena', 'Caroyln', 'Colby', 'Janey', 'Etsuko', 'Renetta', 'Usha', 'Glynis', 'Elvin']
                var surnames = ['Manuel', 'Burkhardt', 'Hart', 'Chavez', 'Bledsoe', 'Stanley', 'Leger', 'Husband', 'Siebold', 'Witt', 'Brown', 'Hammons', 'Rosado', 'Laforest', 'Herrmann', 'Marchese', 'Radford', 'Hartman', 'Farrell', 'Watson', 'Catrone', 'Lawson', 'Edwards', 'Hollon', 'Bolden', 'Golding', 'Marshall', 'Yokley', 'Baumgardner', 'Woodward', 'Miller', 'Crabtree', 'Carter', 'Pierce', 'Deck', 'Bowlin', 'Murray', 'Qualls', 'Ware', 'Wilmoth', 'Trevino', 'Oshey', 'Albee', 'Blackwell', 'Divers', 'Harris', 'Norgard', 'Sullivan', 'Flemming', 'Mccright', 'Poche', 'Kleckner', 'Graffagnino', 'Hudson', 'Diggs', 'Rivera', 'Butler', 'Faulk', 'Woodby', 'Hernandez', 'Frazier', 'Hicks', 'Shelton', 'Council', 'Ferguson', 'Taylor', 'Serbus', 'Wallace', 'Lewis', 'Holland', 'Canada', 'Franklin', 'Tobin', 'Krys', 'Lees', 'Gow', 'Engemann', 'Smith', 'Driscoll', 'Mcinnis', 'Mullen', 'Peterson', 'Leavitt', 'Benefiel', 'Meeks', 'Parker', 'Williams', 'Martin', 'Lagrone', 'Parham', 'Goree', 'Brooks', 'Sauvageau', 'Roeger', 'Boelter', 'Wells', 'Lara', 'Mitchell', 'Bell', 'Young', 'Jordan', 'Singleton', 'Flores', 'Shockley', 'Palesano', 'Sandoval', 'Poole', 'Starr', 'Darby', 'Hetrick', 'Munson', 'Rega', 'Bailey', 'Koch', 'Meagher', 'Krummel', 'Lee', 'Fluitt', 'Gilkes', 'Barnes', 'Crenshaw', 'Rainey', 'Chang', 'Medina', 'Vanacore', 'Murphy', 'Kuttner', 'Steed', 'Padgett', 'Crockett', 'White', 'Ungaro', 'Craig', 'Valsin', 'Jackson', 'Tratar', 'Putman', 'Swartzentrube', 'Stivers', 'Wood', 'Douds', 'Perry', 'Gray', 'Lapage', 'Wallerich', 'Harrigan', 'Poling', 'Alston', 'Nelson', 'Springfield', 'Walker', 'Minks', 'Butcher', 'Mcray', 'Duran', 'Neveu', 'Blanchard', 'Broussard', 'Ikeda', 'Woods', 'Brode', 'Warren', 'Leon', 'Galinis', 'Campbell', 'Brumbaugh', 'Garcia', 'Page', 'Coombs', 'Grimaldo', 'Nolan', 'Gonce', 'Dempster', 'Wheeler', 'Novak', 'Winfield', 'Milano', 'Logan', 'Perillo', 'Gresham', 'Wilson', 'Harrell', 'Bishop', 'Greene', 'Hanks', 'Chapman', 'Guidice', 'Wilcox', 'Burke', 'Dodson', 'Nabb', 'Waggner', 'Eichhorn', 'Meadows', 'Anderson', 'Armor', 'Drew', 'Maxwell', 'Loveland', 'Redd', 'Friedrichs', 'Willard', 'Martinez', 'Treible', 'Duckworth', 'Jones', 'Mcclendon', 'Shah', 'Adams', 'Cartwright', 'Stroud', 'Morris', 'Uccio', 'Johnson', 'Judge', 'Groves', 'Townsley', 'Mory', 'Whitaker', 'Kim', 'Cannon', 'Grumet', 'Houser', 'Sigman', 'Meyers', 'Strickland', 'Kues', 'Andujar', 'Cooper', 'Violet', 'Baber', 'Lair', 'Raiola', 'Pendergast', 'York', 'Clark', 'Huerta', 'Soto', 'Scruggs', 'Harvey', 'Harrison', 'Byrd', 'Fagen', 'Whitten', 'Phillips', 'Borges', 'Mckinley', 'Hollis', 'Winter', 'Deyo', 'Tompkins', 'Hamilton', 'Collings', 'Kaufman', 'Noble', 'Armstrong', 'Priebe', 'Lindhorst', 'Kendrick', 'Sanders', 'Sample', 'Decosta', 'Voss', 'Kowalczyk', 'Decambra', 'Kjelland', 'Valenzuela', 'Ruble', 'Schneider', 'Mazur', 'Henderson', 'Harmon', 'Tartaglione', 'Etheredge', 'Gold', 'Lopez', 'Nickerson', 'Nadeau', 'Conrad', 'Wulf', 'Mckinney', 'Wooden', 'Strong', 'Ashley', 'Whittington', 'Garza', 'Domke', 'Rembert', 'Rosenberg', 'Mclean', 'Luckow', 'Keller', 'Millet', 'Railsback', 'Davis', 'Vizzi', 'Darden', 'Sanchez', 'Rodriguez', 'Culbertson', 'Kleine', 'Casano', 'Hawkins', 'Black', 'Bleakley', 'Bookhardt', 'Gamez', 'Gallagher', 'Almond', 'Schwein', 'Browning', 'Jeffrey', 'Porter', 'Montgomery', 'Scurry', 'Parks', 'Collins', 'Goodwin', 'Cole', 'Wright', 'John', 'Ruiz', 'Kozak', 'Ryan', 'Doemelt', 'Zimmer', 'Durrant', 'Rexrode', 'Wilkins', 'Stewart', 'Haws', 'Gregory', 'Owston', 'Schull', 'Hess', 'Boshard', 'Theroux', 'Ornelas', 'Monteagudo', 'Robison', 'Boeding', 'Aguirre', 'Allen', 'Booth', 'Willis', 'Bills', 'Roop', 'Deluna', 'Freeman', 'Lyford', 'Ripka', 'Archie', 'Carlos', 'Wojciak', 'Ransdell', 'Castro', 'Troke', 'Chalender', 'Griffin', 'Schultz', 'Gamboa', 'Cato', 'Newman', 'Quashie', 'Dufresne', 'Shields', 'Marotta', 'Vang', 'Clerk', 'Granderson', 'Little', 'Pamperin', 'Richards', 'Arnold', 'Hodges', 'Tedrow', 'Silver', 'Fulton', 'Burgess', 'Hutchison', 'Tutt', 'Ortiz', 'Velez', 'Scorgie', 'Lima', 'Meyer', 'Castilo', 'Shafer', 'Griffith', 'Rowland', 'Sherwood', 'Bacher', 'Bridges', 'Plotts', 'Lester', 'Rinehart', 'Chandler', 'Samayoa', 'Boggess', 'Lapierre', 'Dorris', 'Mcrary', 'Cromwell', 'Aleo', 'Beam', 'Breden', 'Lickliter', 'Cronin', 'Cilenti', 'Fitzpatrick', 'Harlan', 'Ohl', 'Cotter', 'Groth', 'Padilla', 'Zuniga', 'Eley', 'Curran', 'Larkin', 'Badman', 'Uplinger', 'Randolph', 'Dyke', 'Greer', 'Kennedy', 'Scott', 'Herron', 'Leggett', 'Hahn', 'Welch', 'Deveau', 'Caldera', 'Kinard', 'Pelton', 'Numbers', 'Moore', 'Metzger', 'Tardiff', 'Bowman', 'Vo', 'Malone', 'Pratt', 'Lockwood', 'Grev', 'Canales', 'Rickey', 'Garlock', 'Rains', 'Carroll', 'Dewan', 'Hunsberger', 'David', 'Vargas', 'Hector', 'Trombetta', 'Gagnon', 'Kittel', 'Dungan', 'Jacobs', 'Edmundson', 'Harrington', 'Keyes', 'Thomason', 'Carpenter', 'Burroughs', 'Barnett', 'Gualtieri', 'Mcdonald', 'Zamora', 'Cohen', 'Maldonado', 'Stevenson', 'Burks', 'Cooke', 'Truax', 'Kulikowski', 'Green', 'Roberts', 'Chaney', 'Bedolla', 'Mullins', 'Okura', 'Huffman', 'Fahy', 'Zalewski', 'Lennon', 'Dingess', 'Russom', 'Hays', 'Lemmon', 'Myers', 'Hendricks', 'Echols', 'Hegyi', 'Tobar', 'Elwick', 'Vallejo', 'Colegrove', 'Vogler', 'Burlin', 'Lowell', 'Rech', 'Rayford', 'Cabler', 'Rudy', 'Warkentin', 'Bruderer', 'King', 'Mcmanus', 'Molina', 'Clemmons', 'Haas', 'Richardson', 'Mallard', 'Beltrami', 'Reyes', 'Glover', 'Robertson', 'Turner', 'Swanson', 'Goetz', 'Robinson', 'Marin', 'Stauffer', 'Huey', 'Kobayashi', 'Thomas', 'Salas', 'West', 'Sayed', 'Koon', 'Ray', 'Kemper', 'Howell', 'Baker', 'Dagley', 'Avila', 'Felicano', 'Runyon', 'Janick', 'Owens', 'Villareal', 'Brislin', 'Buchanan', 'Slowinski', 'Stephens', 'Granger', 'Daily', 'Lawrence', 'Conn', 'Streeter', 'Creager', 'Fowler', 'Wilenkin', 'Russell', 'Grace', 'Wedgewood', 'Hurley', 'Whiteman', 'Olivares', 'Shoup', 'Wolfe', 'Reed', 'Corrigan', 'Byrge', 'Eldridge', 'Woodie', 'Few', 'Mahoney', 'Edmonds', 'Pimentel', 'Boggioni', 'Schmitz', 'Bennerson', 'Zarate', 'Gorman', 'Holloway', 'Minchew', 'Coker', 'Siebert', 'Gholston', 'Bryant', 'Bennett', 'Montijo', 'Felver', 'Cornett', 'Chilton', 'Fox', 'Boucher', 'Rios', 'Samaniego', 'Delamora', 'Plummer', 'Becker', 'Mcninch', 'Henry', 'Davila', 'Mcrae', 'Armitage', 'Maxham', 'Huhman', 'Graves', 'George', 'Finke', 'Segovia', 'Bond', 'Kurtz', 'Olson', 'Clacher', 'Potts', 'Cadorette', 'Day', 'Wilkinson', 'Iredale', 'Wenz', 'Lamar', 'Capdeville', 'Martello', 'Dillon', 'Melgar', 'Pigford', 'Carrington', 'Ross', 'Hollinger', 'Nielsen', 'Dempsey', 'Hailey', 'Gaston', 'Gonzales', 'Moyer', 'Duffy', 'Estes', 'Patten', 'Mccord', 'Lanning', 'Perez', 'Pruitt', 'Rowan', 'Kimme', 'Morton', 'Beck', 'Mcbride', 'Doverspike', 'Hix', 'Gonzalez', 'Crigger', 'Gardner', 'Baver', 'Stafford', 'Elliott', 'Mummert', 'Rochester', 'Summey', 'Yeung', 'Matos', 'Desoto', 'Bartley', 'Dorman', 'Langlinais', 'Jiles', 'Currin', 'Tunstall', 'Morrison', 'Cokely', 'Kirk', 'Kondracki', 'Baldwin', 'Vance', 'Steele', 'Kinkelaar', 'Sermersheim', 'Gill', 'Mcbee', 'Harrold', 'Jewett', 'Duvall', 'Ivery', 'Turben', 'Alexander', 'Dumas', 'Patterson', 'Mendez', 'Moen', 'Embry', 'Jemison', 'Cantrell', 'Keen', 'Howard', 'Clemons', 'Pullen', 'Burpo', 'Oney', 'Stiff', 'Hunter', 'Lehnen', 'Ebinger', 'Chan', 'Hanson', 'Bye', 'Abbe', 'Tinney', 'Poland', 'Powell', 'James', 'Cassidy', 'Baxley', 'Dale', 'Harling', 'Kornegay', 'Lightsey', 'Crawley', 'Bartz', 'Emmons', 'Bollinger', 'Barrett', 'Mann', 'Schanz', 'Agosta', 'Hannon', 'Corbin', 'Ehret', 'Cox', 'Nittler', 'Douglass', 'Larocco', 'Royster', 'Norman', 'Labadie', 'Dewing', 'Kinnaman', 'Everett', 'Tacadina', 'Shinabarger', 'Diederich', 'Fellin', 'Larson', 'Dacey', 'Flynn', 'Cortez', 'Ferrell', 'Vanzee', 'Cruz', 'Satterwhite', 'Stutts', 'Lynch', 'Jencks', 'Johnsen', 'Joyce', 'Dawes', 'Chisolm', 'Preston', 'Hines', 'Stinson', 'Thrill', 'Wilkes', 'Peatross', 'Fasciano', 'Czelusniak', 'Saylors', 'Smittle', 'Lachance', 'Schock', 'Haddad', 'Sondrini', 'Kilpatrick', 'Feasel', 'Tso', 'Vigil', 'Hucks', 'Tasker', 'Goldie', 'Church', 'Reece', 'Guzman', 'Moffatt', 'Tuttle', 'Yarbrough', 'Wilkerson', 'Kirkwood', 'Mckenna', 'Hefner', 'Holt', 'Pederson', 'Tsang', 'Rupp', 'Dendy', 'Satterthwaite', 'Keeney', 'Pease', 'Manning', 'Chamberland', 'Higgins', 'Oglesby', 'Wolverton', 'Benbow', 'Brennan', 'Grant', 'Mills', 'Timmons', 'Marriner', 'Reeder', 'Robbins', 'Luker', 'Berrios', 'Partlow', 'Uong', 'Ewing', 'Estey', 'Berezny', 'Golden', 'Schroeder', 'Dalrymple', 'Pfister', 'Ruper', 'Gennaro', 'Aragon', 'Clarke', 'Chavarria', 'Heberling', 'Laramie', 'Pair', 'Spilde', 'Noyes', 'Seevers', 'Mick', 'Street', 'Heckel', 'Clair', 'Long', 'Hengl', 'Santiago', 'Mcfarlane', 'Gustafson', 'Hollabaugh', 'Greenfield', 'Ratcliff', 'Culotta', 'Ruffner', 'Quick', 'Doll', 'Holmes', 'Womer', 'Franks', 'Pautz', 'League', 'Siddall', 'Andersen', 'Marcano', 'Fernandez', 'Davidson', 'Graham', 'Matthews', 'Rosson', 'Huether', 'Gantz', 'Gilbert', 'Valentin', 'Coulter', 'Navarro', 'Weber', 'Snow', 'Newell', 'Askew', 'Dixon', 'Mcelroy', 'Swackhammer', 'Styron', 'Samples', 'Gallego', 'Park', 'Gifford', 'Oswald', 'Eilerman', 'Doyle', 'Hobby', 'Barclay', 'Kettler', 'Bouton', 'Bramlet', 'Cavender', 'Garrison', 'Bilbo', 'Fields', 'Mcdaniel', 'Sosa', 'Arteaga', 'Hayes', 'Lindblad', 'Peters', 'Underwood', 'Sims', 'Mcgillivray', 'Rigby', 'Mickey', 'Weldon', 'Sergi', 'Placko', 'Strang', 'Niss', 'Buchmeier', 'Natividad', 'Blassingame', 'Hall', 'Culver', 'Wagner', 'Quiggle', 'Rich', 'Dame', 'Parisien', 'Carlson', 'Ramos', 'Tremblay', 'Hintz', 'Petillo', 'Combs', 'Zanella', 'Doan', 'Beavers', 'Sill', 'Logsdon', 'Medlin', 'Singley', 'Grap', 'Burns', 'Lord', 'Wohlrab', 'Bedford', 'Marden', 'Chin', 'Ricketts', 'Hodgdon', 'Lovisone', 'Weaver', 'Leusink', 'Grisham', 'Alfred', 'Tardy', 'Speer', 'Raio', 'Spragg', 'Larochelle', 'Booker', 'Bodenhamer', 'Eck', 'Mcnamara', 'Villalvazo', 'Abel', 'Mettlen', 'Roman', 'Lapointe', 'Leblond', 'Huntington', 'Major', 'Aker', 'Mosley', 'Monroy', 'Thibeault', 'Harper', 'Derouen', 'Perrigo', 'Huff', 'Crowe', 'Moser', 'Bradley', 'Ford', 'Overton', 'Keppler', 'Bush', 'Pruzansky', 'Flatter', 'Bettencourt', 'Kraus', 'Farley', 'Hill', 'Walter', 'Hoyt', 'Olague', 'Treisch', 'Knickrehm', 'Evans', 'Foster', 'Stevens', 'Viernes', 'Delgado', 'Willick', 'Mcintyre', 'Garton', 'Morse', 'Casagrande', 'Mattera', 'Ruff', 'Boggs', 'Greenwood', 'Mcwilliams', 'Wiley', 'Shay', 'Gunderman', 'Cotton', 'Buchheit', 'Rogalski', 'Zepeda', 'Massaro', 'Parsons', 'Zepp', 'Puckett', 'Rock', 'Sparkman', 'Vanicek', 'Newcomb', 'Purcell', 'Steverson', 'Farmer', 'Leuthold', 'Mcchristian', 'Igel', 'Minge', 'Frew', 'Mullet', 'Thornton', 'Eld', 'Burton', 'Hansen', 'Rollison', 'Bates', 'Ngo', 'Lozano', 'Barney', 'Matson', 'Colella', 'Mccoy', 'Meaker', 'Stratton', 'Unsworth', 'Blackburn', 'Maiden', 'Vasquez', 'Aman', 'Phelps', 'Mesa', 'Rinck', 'Bourg', 'Riding', 'Cable', 'Eichberger', 'May', 'Spears', 'Burris', 'Sallas', 'Rudzinski', 'Yang', 'Cavazos', 'Sacco', 'Rojas', 'Jorge', 'Meade', 'Rosemond', 'Whitehead', 'Botz', 'Brookman', 'Szabo', 'Grullon', 'Hunt', 'Camacho', 'Kerr', 'Abernathy', 'Elliam', 'Handelman', 'Hubbard', 'Jelks', 'Morlan', 'French', 'Landreneau', 'Stephen', 'Heimbach', 'Okeefe', 'Stout', 'Capehart', 'Roy', 'Dominguez', 'Schaeffer', 'Austin', 'Corcoran', 'Waldron', 'Dammen', 'Barcia', 'Peco', 'Chaffin', 'Pitts', 'Laird', 'Sandoz', 'Wibbens', 'Quimby', 'Elrod', 'Maus', 'Regalado', 'Beachy', 'Menze', 'Oneal', 'Hyde', 'Robleto', 'Colon', 'Lytle', 'Shorter', 'Jondle', 'Ward', 'Pitt', 'Degrate', 'Borgen', 'Keding', 'Siegfried', 'Winters', 'Talbert', 'Stucker', 'Hausmann', 'Elmore', 'Bergan', 'Kostrzewa', 'Seales', 'Rush', 'Hebel', 'Perryman', 'Rather', 'Wall', 'Pritchett', 'Horne', 'Mahaffey', 'Bonds', 'Barragan', 'Moochler', 'Jernigan', 'Love', 'Godeaux', 'Carson', 'Widger', 'Early', 'Terry', 'Benson', 'Sheahan', 'Hobbs', 'Haskell', 'Wedel', 'Letarte', 'Monroe', 'Hardy', 'Honokaupu', 'Shock', 'Oakley', 'Gomes', 'Rhodes', 'Schmidt', 'Tobias', 'Loomis', 'Lovett', 'Alcorn', 'Lang', 'Aguilar', 'Dean', 'Woolbright', 'Harrelson', 'Hutzler', 'Bovee', 'Curtis', 'Wise', 'Pinilla', 'Vinson', 'Gaydosh', 'Pfaff', 'Jenkins', 'Chiquito', 'Thomlinson', 'Huynh', 'Schumaker', 'Micks', 'Trinh', 'Nealon', 'Rivers', 'Newton', 'Mcfarland', 'Morano', 'Valdivia', 'Couture', 'Simpkins', 'Ramin', 'Franke', 'Hornsby', 'Pennick', 'Sato', 'Reik', 'Silva', 'Warman', 'Therrien', 'Heslop', 'Randell', 'Heckert', 'Logiudice', 'Vansice', 'Gannon', 'Stokes', 'Reilly', 'Nalley', 'Akerley', 'Braziel', 'Nicoletti', 'Comstock', 'Handley', 'Fletcher', 'Rizo', 'Jenson', 'Raper', 'Weiler', 'Ogorman', 'Pointer', 'Brunson', 'Andrade', 'Mirando', 'Mckeithan', 'Shanholtzer', 'Quigley', 'Whitson', 'Talley', 'Friedle', 'Krause', 'Hackman', 'Griggs', 'Dowd', 'Gillette', 'Crislip', 'Gamble', 'Lundholm', 'Kalas', 'Plourde', 'Christensen', 'Lue', 'Horton', 'Fissel', 'Leach', 'Toothman', 'Rothfuss', 'Kimbrough', 'Dyer', 'Maass', 'Stricklin', 'Dumlao', 'Jasso', 'Janecka', 'Leatherman', 'Hoggins', 'Guerrero', 'Doe', 'Casady', 'Reyna', 'Kelty', 'Glaser', 'Tuite', 'Boudreaux', 'Malmquist', 'Otis', 'Abe', 'Daudelin', 'Handy', 'Mathews', 'Haynes', 'Vaux', 'Wegman', 'Pharmer', 'Troublefield', 'Coots', 'Vandre', 'Showe', 'Westerberg', 'Gelabert', 'Wildey', 'Joe', 'Torres', 'Jacques', 'Hogue', 'Hotaling', 'Deshazer', 'Pepin', 'Neville', 'Ezzelle', 'Schmit', 'Dudley', 'Guillory', 'Hedrick', 'Palmer', 'Sneed', 'Sharpe', 'Hankin', 'Diamond', 'Heinz', 'Cacciatori', 'Shanahan', 'Lutz', 'Marsh', 'Hilton', 'Wires', 'Zimmermann', 'Sexton', 'Washington', 'Stuzman', 'Cathey', 'Teel', 'Brewer', 'Daniels', 'Gough', 'Pimental', 'Shaw', 'Burger', 'Lockett', 'Trentman', 'Velasco', 'Stclair', 'Mezick', 'Bauer', 'Soron', 'Timberlake', 'Coll', 'Salmi', 'Bousquet', 'Salinas', 'Hite', 'Li', 'Sleeper', 'Abarca', 'Fleeman', 'Woodcock', 'Price', 'Grimm', 'Pires', 'Lagunas', 'Fisher', 'Smart', 'Akbar', 'Lloyd', 'Mitchener', 'Gadson', 'Potolsky', 'Beamish', 'Caruthers', 'Garber', 'Hendrickson', 'Osborn', 'Dacosta', 'Nguyen', 'Chapa', 'Acker', 'Boyd', 'Delaney', 'Morgan', 'Lepley', 'Skipper', 'Todd', 'Crouse', 'Parson', 'Wilbourne', 'Net', 'Winston', 'Casas', 'Mcmurray', 'Ellerbe', 'Terrell', 'Cowie', 'Mcmorris', 'Dickens', 'Walters', 'Gentry', 'Perham', 'Glass', 'Dowling', 'Vires', 'Gutierrez', 'Ingram', 'Woodard', 'Helgeson', 'Neil', 'Marshal', 'Brunette', 'Vrba', 'Bedgood', 'Albright', 'Horn', 'Amador', 'Wolf', 'Sandrock', 'Pardo', 'Guevara', 'Mcclelland', 'Gartner', 'Hernande', 'Deeter', 'Winkles', 'Kapur', 'Paiz', 'Devore', 'Mcquay', 'Jutras', 'Caballero', 'Ruano', 'Sutphin', 'Maks', 'Beard', 'Culbreth', 'Noel', 'Salvemini', 'Fuller', 'Prince', 'Bayardo', 'Good', 'Seling', 'Ricker', 'Zbell', 'Hanchett', 'Abuaita', 'Banks', 'Gaddie', 'Hagstrom', 'Bartlett', 'Rosa', 'Head', 'Carmichael', 'Burtner', 'Hasbrouck', 'Rogers', 'Urankar', 'Ries', 'Link', 'Baptist', 'Cornelius', 'Dillard', 'Henson', 'Whitney', 'Hower', 'Hughes', 'Mcginnis', 'Harkavy', 'Tooley', 'Atwood', 'Westbrook', 'Brackley', 'Scudder', 'Webster', 'Needleman', 'Obermeyer', 'Stolar', 'Gammage', 'Williamson', 'Hassard', 'Mcneely', 'Mcclure', 'Hope', 'Lerner', 'Melody', 'Bankard', 'Bogan', 'Satterfield', 'Byers', 'Julius', 'Runnels', 'Stott', 'Mccormick', 'Roddy', 'Moses', 'Provence', 'Leech', 'Sadler', 'Webb', 'Small', 'Hennessey', 'Rathbone', 'Moss', 'Worker', 'Lindsay', 'Adami', 'Mercer', 'Ryburn', 'Anthony', 'Britton', 'Basinski', 'Morter', 'Sutton', 'Rose', 'Barber', 'Kowalcyk', 'Cherian', 'Hampton', 'Scheumann', 'Velis', 'Pardee', 'Renfro', 'Humphrey', 'Pryor', 'Cifelli', 'Wolcott', 'Bowser', 'Welsh', 'Brooke', 'Koehler', 'Sedlacek', 'Strope', 'Degasperis', 'Locke', 'Landry', 'Burk', 'Wiemer', 'Quintanilla', 'Yardley', 'Coleman', 'Blair', 'Araujo', 'Mumbower', 'Ruthledge', 'Olds', 'Jarvis', 'Bronson', 'Weisner', 'Runion', 'Grennan', 'Pohlman', 'Marion', 'Mcgovern', 'Sale', 'Schwenke', 'Fanney', 'Cass', 'Chau', 'Liberty', 'Brinkley', 'Creel', 'Brand', 'Lotton', 'Wilmot', 'Bova', 'Ovando', 'Lacey', 'Coryell', 'Pollard', 'Joubert', 'Erdmann', 'Bundy', 'Kama', 'Blaze', 'Frye', 'Nunes', 'Myhre', 'Thompson', 'Petree', 'Lamper', 'Krumwiede', 'Fischer', 'Spillett', 'Gaskill', 'Caldwell', 'Hash', 'Yates', 'Couts', 'Dill', 'Ly', 'Sughrue', 'Petrus', 'Santo', 'Amaya', 'Sutter', 'Mccleskey', 'Langhorne', 'Tomer', 'Weuve', 'Mcentire', 'Bender', 'Berry', 'Raymond', 'Angelocci', 'Gautreau', 'Walsh', 'Parmley', 'Gronewald', 'Mcneill', 'Heming', 'Fayne', 'Camilo', 'Sung', 'Kemmis', 'Lujan', 'Tisdale', 'Krier', 'Akins', 'Merida', 'Glenn', 'Inman', 'Mendoza', 'Botts', 'Lyall', 'Monti', 'Riddell', 'Zenger', 'Gaddy', 'Dupes', 'Viteri', 'Manser', 'Brummell', 'Valenzula', 'Wisdom', 'Adelman', 'Fitzsimmons', 'Causey', 'Waterhouse', 'Harman', 'Hobson', 'Pickle', 'Keys', 'Westlie', 'Breen', 'Espinosa', 'Hollingsworth', 'Shannon', 'Shedlock', 'Corrie', 'Gottfried', 'Gaters', 'Swallow', 'Fruits', 'Huss', 'Patchell', 'Arevalo', 'Dorsey', 'Packard', 'Hooper', 'Vazquez', 'Kostiuk', 'Swindell', 'Pon', 'Alford', 'Baptiste', 'Hoey', 'Coffee', 'Mcenaney', 'Spalding', 'Barrier', 'Cormier', 'Carr', 'Creasman', 'Carey', 'Geiger', 'Cropsey', 'Johansen', 'Ayers', 'Meek', 'Delrio', 'Shea', 'Fugate', 'Davenport', 'Fennell', 'Kehoe', 'Schrag', 'Hacher', 'Alcala', 'Yandell', 'Mckenzie', 'Toliver', 'Slay', 'Rumpf', 'Harstad', 'Durfee', 'Conorich', 'Sagen', 'Carney', 'Rachal', 'Sawyer', 'Kane', 'Tart', 'Krumholz', 'Gibson', 'Webber', 'Goldberg', 'Seitz', 'Childers', 'Orozco', 'Whedbee', 'Beliveau', 'Medeiros', 'Jimenez', 'Sewell', 'Filip', 'Base', 'Torrez', 'Kling', 'Pearson', 'Burrell', 'Reveles', 'Mcgrath', 'Riddick', 'Breitenbach', 'Hadley', 'See', 'Wang', 'Steelman', 'Mcdearmont', 'Tanner', 'Bigler', 'Alma', 'Ashbaugh', 'Whitefield', 'Mcelderry', 'Stacey', 'Hench', 'Mcnulty', 'Vinci', 'Lavine', 'Heise', 'Sargeant', 'Parsley', 'Mcmullen', 'Olney', 'Vise', 'Bunting', 'Cervantes', 'Castrellon', 'Lindley', 'Sunday', 'Ellis', 'Destina', 'Richie', 'Elder', 'Osbeck', 'Erwin', 'Isola', 'German', 'Susana', 'Gatson', 'Blaser', 'Velazquez', 'Bergeron', 'Dison', 'Vaughn', 'Knight', 'Hallam', 'Amari', 'Looney', 'Janssen', 'Christiansen', 'Medlock', 'Owen', 'Lococo', 'Borders', 'Prickett', 'Caudill', 'Shearer', 'Mercado', 'Batters', 'Steffen', 'Worley', 'Coore', 'Simmons', 'Farris', 'Banh', 'Mulloy', 'Cheslock', 'Lekan', 'Egan', 'Schumacher', 'Turgeon', 'Wuest', 'Foulkes', 'Boyte', 'Klos', 'Rosario', 'Wiseman', 'Stidham', 'Ellison', 'Shockey', 'Alvarez', 'Truman', 'Faison', 'Nabors', 'Contreras', 'Beal', 'Bengtson', 'Billings', 'Shores', 'Reynoso', 'Hollowell', 'Pham', 'Tucker', 'Sanderson', 'Dallas', 'Jonas', 'Barajas', 'Truesdell', 'Millay', 'Ambler', 'Wagoner', 'Friedman', 'Didonato', 'Patrick', 'Krueger', 'Bott', 'Shackelford', 'Sandiford', 'Rice', 'Thurston', 'Mayfield', 'Conner', 'Brady', 'Hoover', 'Eldreth', 'Lockridge', 'Place', 'Mcsweeney', 'Brockett', 'Ponce', 'Pannenbacker', 'Dabney', 'Drake', 'Saltsman', 'Mahon', 'Cook', 'Archila', 'Schroyer', 'Zarek', 'Mistrot', 'Lomax', 'Mcbean', 'Winkelpleck', 'Crase', 'Crocker', 'Wade', 'Gleaves', 'Mcmillian', 'Flowers', 'Hoag', 'Langehennig', 'Neale', 'Hodge', 'Urick', 'Bragg', 'Nicholson', 'Petrocco', 'Hirz', 'Sconiers', 'Mcdowell', 'Skinner', 'Kern', 'Mays', 'Kopka', 'Irvin', 'Leiker', 'Atkeson', 'Loney', 'Belin', 'Estabillo', 'Perrine', 'Aran', 'Hanna', 'Creveling', 'Pina', 'Stahl', 'Chong', 'Nordstrom', 'Anguiano', 'Grayson', 'Meadors', 'Osmond', 'Carbajal', 'Mcconnell', 'Somogyi', 'Kelly', 'Rankin', 'Almand', 'Edson', 'Rubio', 'Brunkhorst', 'Mcclard', 'Christopher', 'Krapp', 'Siegal', 'Spencer', 'Field', 'Callis', 'Ashland', 'Riley', 'Rudloff', 'Parr', 'Morin', 'Russ', 'Rood', 'Ho', 'Yohn', 'Uriegas', 'Waite', 'Eure', 'Noonan', 'Wachter', 'Woolridge', 'Younker', 'Fountain', 'Patton', 'Degregorio', 'Gorton', 'Brucculeri', 'Murdoch', 'Emery', 'Gartin', 'Barry', 'Monton', 'Richter', 'Powers', 'Grunden', 'Butterfield', 'Lockard', 'Mancia', 'Schuller', 'Priem', 'Sharp', 'Yancik', 'Stansbury', 'Petit', 'Romano', 'Schacht', 'High', 'Coley', 'Gladwell', 'Cain', 'Perrella', 'Stoker', 'Watley', 'Retchless', 'Fraction', 'Gagne', 'Lacount', 'Gates', 'Sharon', 'Cross', 'Bowen', 'Dolan', 'Petty', 'Seanez', 'Lavigne', 'Finley', 'Frasier', 'Angeles', 'Pounds', 'Spengler', 'Tait', 'Richburg', 'Humphries', 'Albaugh', 'Hamm', 'Boulton', 'Aldred', 'Carlton', 'Hebert', 'Ligon', 'Fant', 'Best', 'Whelan', 'Jacinto', 'Mcspadden', 'Dong', 'Levin', 'Dehn', 'Reisinger', 'Gooden', 'Gable', 'Luis', 'Ribeiro', 'Waring', 'Murrell', 'Balagtas', 'Holliman', 'Heier', 'Whipple', 'Emberton', 'Floyd', 'Escobedo', 'Longbrake', 'Tesoriero', 'Christian', 'Bisom', 'Deutsch', 'Delacruz', 'Schermann', 'Villa', 'Clay', 'Crouch', 'Dupree', 'Short', 'Starks', 'Ferreira', 'Escamilla', 'Liggett', 'Summers', 'Corbitt', 'Templeton', 'Teague', 'Reese', 'Aguiar', 'Minnick', 'Almendarez', 'Hickerson', 'Healy', 'Steagell', 'Pearce', 'Peterman', 'Watkins', 'Malloy', 'Eversmeyer', 'Meecham', 'Jobe', 'Rollinger', 'Blakeley', 'Bencomo', 'Simms', 'Canty', 'Schaefer', 'Marmerchant', 'Stowell', 'Bull', 'Boone', 'Whitlow', 'Bateman', 'Mckee', 'Korsak', 'Barnhill', 'Cochran', 'Middleton', 'Acosta', 'Washburn', 'Sala', 'Emerson', 'Hood', 'Bernard', 'Macleod', 'Demopoulos', 'Lemmons', 'Rau', 'Hoeppner', 'Roa', 'Sjolander', 'Hedtke', 'Gunstream', 'Luoma', 'Swedenburg', 'Woodhouse', 'Widener', 'Holbrook', 'Bagger', 'Honeycutt', 'Linder', 'Billy', 'Ledesma', 'Mcgary', 'Barner', 'Meacham', 'Townsend', 'Lovette', 'Krajcer', 'Diaz', 'Darling', 'Hathaway', 'Yingling', 'Pineda', 'Becerra', 'Pena', 'Kendall', 'Nichols', 'Sylvester', 'Snook', 'Babcock', 'Reynolds', 'Masztal', 'Lummus', 'Daugherty', 'Kelso', 'Haywood', 'Schrecongost', 'Swinson', 'Niles', 'Mclendon', 'Leath', 'Mortensen', 'Prichard', 'Bonner', 'Vroman', 'Heinlen', 'Rendon', 'Itson', 'Marr', 'Grimes', 'Roe', 'Collette', 'Eddy', 'Cleckner', 'Ramsdell', 'Grate', 'Burwell', 'Battaglia', 'Merrill', 'Coelho', 'Constant', 'Castle', 'Zertuche', 'Hutchens', 'Walls', 'Torrence', 'Paider', 'Luther', 'Saeler', 'Toscano', 'Villasenor', 'Eng', 'Rae', 'Barba', 'Thibeaux', 'Thornbury', 'Peacemaker', 'Gillis', 'Ota', 'Roller', 'Shierling', 'Crigler', 'Randall', 'Brassil', 'Morales', 'Curb', 'Moreno', 'Georges', 'Bernier', 'Englehardt', 'Knott', 'Hance', 'Sandow', 'Galbreath', 'Whit', 'Nettles', 'Waggoner', 'Mcdougald', 'Whitton', 'Bray', 'Claeys', 'Laurent', 'Canale', 'Perrez', 'Boykin', 'Schluter', 'Sparks', 'Fraga', 'Mcghee', 'Baird', 'Sledge', 'Scofield', 'Taulbee', 'Biron', 'Mulligan', 'Kemp', 'Beumer', 'Zimmerman', 'Bustamante', 'Reeves', 'Burnett', 'Lade', 'Boston', 'Nunn', 'Illuzzi', 'Dingell', 'Mcnally', 'Crane', 'Cunningham', 'Brund', 'Staples', 'Akers', 'Onisick', 'Wehn', 'Bostic', 'Colucci', 'Calton', 'Pyron', 'Maye', 'Mackenzie', 'Hazelton', 'Sclafani', 'Heavner', 'Morrissey', 'Bartelt', 'Sills', 'Griffiths', 'Paige', 'Juba', 'Richmond', 'Peel', 'Singelton', 'Heard', 'Siemens', 'Morrical', 'Rao', 'Pedersen', 'Mines', 'Franch', 'Ballard', 'Cancilla', 'Irons', 'Pollick', 'Godfrey', 'Kaiser', 'Jung', 'Bennet', 'Samuel', 'Mccalpane', 'Cleary', 'Stacy', 'Melton', 'Timm', 'Brinton', 'Decinti', 'Garth', 'Stiles', 'Herold', 'Ahrens', 'Tauras', 'Melchor', 'Bornhorst', 'Barnette', 'Gomez', 'Jamison', 'Aleman', 'Rolf', 'Rautenstrauch', 'Lucas', 'Hornlein', 'Estep', 'Uber', 'Niemi', 'Mandala', 'Flaherty', 'Schmelz', 'Berg', 'Hurt', 'Pardun', 'Caligiuri', 'Lane', 'Reinhardt', 'Perotti', 'Drewett', 'Dowell', 'Zody', 'Garner', 'Galiano', 'Fisk', 'Perrington', 'Abbasi', 'Obrian', 'Moniz', 'Macintyre', 'Ankney', 'Gallardo', 'Urbina', 'Shambo', 'Faulkner', 'Laferriere', 'Nunez', 'Copeland', 'Allan', 'Hadlock', 'Crowell', 'Cobb', 'Gummer', 'Wilke', 'Melvin', 'Atkins', 'Otero', 'Goldstein', 'Buel', 'Chung', 'Thon', 'Watts', 'Mckoy', 'Zirin', 'Crossman', 'Harding', 'Valdez', 'Connors', 'Broadway', 'Puotinen', 'Dyches', 'Waterman', 'Mayhew', 'Sweeney', 'Grothe', 'Rangel', 'Lamon', 'Mcleod', 'Isaacs', 'Eisenberg', 'Medellin', 'Osburn', 'Broadnax', 'Dunn', 'Bojorquez', 'Herrera', 'Cann', 'Popp', 'Milbourn', 'Roberson', 'Palacios', 'Tran', 'Partridge', 'Scianna', 'Mason', 'Cavin', 'Tinsley', 'Mooney', 'Roques', 'Tejada', 'Gomer', 'Lefkowitz', 'Hurst', 'Scolaro', 'Tesch', 'Mcculley', 'Connell', 'Walton', 'Alvarado', 'Mccauley', 'Shelly', 'Boswell', 'Evenson', 'Benton', 'Mata', 'Ritzman', 'Ayala', 'Sayle', 'Vincent', 'Brede', 'Foor', 'Spruill', 'Keomuangtai', 'Eckart', 'Mccrary', 'Mcglothian', 'Hust', 'Stock', 'Barth', 'Goldblatt', 'Leonard', 'Tiburcio', 'Norrell', 'Roesler', 'Pino', 'Peebles', 'Francis', 'Ebert', 'Eubanks', 'Furman', 'Haggard', 'Dawson', 'Bouchard', 'Heikes', 'Ragan', 'Bissell', 'Yu', 'Parry', 'Yoho', 'Paduano', 'Willet', 'Springs', 'Beddo', 'Silvia', 'Sargent', 'Hoskins', 'Diehl', 'Nealey', 'Sain', 'Kendal', 'Rama', 'Spelman', 'Hagen', 'Tennyson', 'Madlung', 'Horth', 'Maciver', 'Brueggeman', 'Gallo', 'Mawyer', 'Robyn', 'Sampsell', 'Stone', 'Dingle', 'Scheller', 'Winfrey', 'Delossantos', 'Shamblin', 'Dardar', 'Cabrera', 'Stoffel', 'Wanda', 'Berryman', 'Buffin', 'Mcphail', 'Peoples', 'Barker', 'Parra', 'Ramirez', 'Hedgepeth', 'Van', 'Schilling', 'Kridel', 'Flint', 'Pedroza', 'Carreras', 'Montoya', 'Roldan', 'Low', 'Calhoun', 'Carrier', 'Sheffield', 'Simpson', 'Calhoon', 'Blandy', 'Tudela', 'Marsaw', 'Flournoy', 'Donaldson', 'Leischner', 'Holley', 'Ezell', 'Frith', 'Gann', 'Reisner', 'Tarr', 'Mcmann', 'Cano', 'Livingston', 'Tolbert', 'Gant', 'Dawkins', 'Magelssen', 'Zavala', 'Halyk', 'Pascal', 'Frazer', 'Perreault', 'Fredericks', 'Crawford', 'Read', 'Druck', 'Lavis', 'Chittenden', 'Mirza', 'Musgrave', 'Hogan', 'Gee', 'Valentine', 'Cobham', 'Welby', 'Tuggle', 'Filion', 'Cosper', 'Bowers', 'Tibbets', 'Gipson', 'Laux', 'Lemons', 'Nester', 'Malinsky', 'Garrow', 'Proffitt', 'Salmon', 'Brus', 'Haggerty', 'Dahnke', 'Marchan', 'Vogel', 'Dagostino', 'Lotz', 'Solano', 'Dishaw', 'Hopf', 'Oller', 'Baugh', 'Reighard', 'Blay', 'Ledoux', 'Herrington', 'Chidester', 'Picciano', 'Barra', 'Vaccaro', 'Conklin', 'Heisler', 'Taft', 'Opteyndt', 'Salak', 'Kittler', 'Thom', 'Hester', 'Oneill', 'Harbin', 'Perkins', 'Doerr', 'Vereb', 'Dionne', 'Cloutier', 'Zecca', 'Meeter', 'Sasso', 'Jorgensen', 'Wyatt', 'Overbey', 'Crafford', 'Travis', 'Pao', 'Guerra', 'Escalante', 'Labarre', 'Riso', 'Titus', 'Holman', 'Aucoin', 'Kittinger', 'Krantz', 'Colburn', 'Ochwat', 'Duskey', 'Martel', 'Heath', 'Kennard', 'Mirsky', 'Giorgio', 'Helms', 'Champine', 'Nieves', 'Lurry', 'Pelletier', 'Shiner', 'Adamson', 'Judd', 'Posner', 'Johns', 'Coria', 'Edge', 'Sand', 'Philips', 'Mascarenas', 'Foley', 'Spalla', 'Krasley', 'Vissering', 'Redway', 'Blake', 'Capps', 'Dunnington', 'Grobmyer', 'Resner', 'Decker', 'Basil', 'Penton', 'Binkley', 'Rodgers', 'Holladay', 'Angel', 'Herrin', 'Mckillip', 'Martich', 'Baez', 'Pater', 'Furnace', 'Cortes', 'Obrien', 'Holtz', 'Blanton', 'Blain', 'Dye', 'Huot', 'Driggers', 'Hadiaris', 'Dimaggio', 'Dutcher', 'Kohnen', 'Coggin', 'Lenning', 'Norris', 'Rodriquez', 'Romanik', 'Oreilly', 'Hager', 'Salvador', 'Whitley', 'Crespo', 'Nilsson', 'Fortier', 'Reidy', 'Rinkel', 'Fallon', 'Cramer', 'Foree', 'Duval', 'Heuschkel', 'Glosson', 'Lam', 'House', 'Tilley', 'Mathison', 'Filgo', 'Giacomini', 'Fuston', 'Bartholf', 'Spiers', 'Ingerson', 'Quarnstrom', 'Laplante', 'Fairhurst', 'Soderberg', 'Getz', 'Boggan', 'Capello', 'Yoder', 'Bella', 'Nobles', 'Fetterolf', 'Mcpherson', 'Colliver', 'Nagel', 'Heber', 'Obermiller', 'Doud', 'Leonetti', 'Dietzel', 'Lamarre', 'Mcquinn', 'Vanderschel', 'Rocha', 'Casad', 'Weinberg', 'Rudd', 'Lowery', 'Mccarver', 'Slack', 'Goodman', 'Hammonds', 'Petro', 'Puente', 'Muto', 'Whistler', 'Kirch', 'Vail', 'Nemeth', 'Otoole', 'Washing', 'Ervin', 'Rashid', 'Aaron', 'Ehrlich', 'Torbett', 'Copple', 'Ohanlon', 'Wriedt', 'Story', 'Lucero', 'Sipes', 'Intrieri', 'Hyman', 'Winburn', 'Sanford', 'Pichette', 'Justiniano', 'Keeton', 'Estrada', 'Belanger', 'Punches', 'Freed', 'Nesby', 'Redman', 'Kittelberger', 'Downing', 'Bunn', 'Russo', 'Sisk', 'Esposito', 'Brock', 'Eyler', 'Ehmann', 'Alamilla', 'Halbert', 'Musial', 'William', 'Struck', 'Hamlin', 'Skelley', 'Land', 'Tibbs', 'Breaux', 'Altom', 'Divine', 'Gibbs', 'Boerger', 'Hurwitz', 'Boyle', 'Merriman', 'Forbes', 'Semaan', 'Lucio', 'Lott', 'Finch', 'Lowman', 'Yancy', 'Fairbairn', 'Losoya', 'Murillo', 'Weinstein', 'Thurman', 'Bessler', 'Terp', 'Briseno', 'Ceja', 'Crandall', 'Guffey', 'Zachary', 'Horr', 'Wilusz', 'Pattee', 'Burney', 'Laughlin', 'Groff', 'Wal', 'Moran', 'Delong', 'Carbo', 'Hartford', 'Rediger', 'Roden', 'Chamberlain', 'Bower', 'Cahill', 'Alaibilla', 'Rhudy', 'Carl', 'Schuler', 'Frontz', 'Harewood', 'Moline', 'Timmerman', 'Orleans', 'Lema', 'Stephenson', 'Bang', 'Woodson', 'Romeo', 'Astorga', 'Snedegar', 'Treadway', 'Traina', 'Toy', 'Agnello', 'Brackett', 'Tolentino', 'Wolfenbarger', 'Broyles', 'Odonell', 'Lockhart', 'Hulett', 'Pinto', 'Arndt', 'Lightner', 'Pitcherello', 'Coburn', 'Vogelgesang', 'Slocum', 'Bolling', 'Mcdonough', 'Culbreath', 'Koski', 'Waddell', 'Inda', 'Brunner', 'Houck', 'Mansfield', 'Matney', 'English', 'Astin', 'Bolin', 'Sartain', 'Reid', 'Purtle', 'Lindquist', 'Sweed', 'Hansing', 'Beyl', 'Wynne', 'Schaedler', 'Kelley', 'Rosner', 'Schuckert', 'Poppel', 'Figueroa', 'Ellinwood', 'Moya', 'London', 'Marquez', 'Manley', 'Hopkins', 'Saunders', 'Abreu', 'Becnel', 'Vidrine', 'Ginsburg', 'Albers', 'Bluestein', 'Payne', 'Angle', 'Cvetkovic', 'Mossman', 'Mcilwain', 'Laduke', 'Rust', 'Smithey', 'Benavidez', 'Demaray', 'Willey', 'Betts', 'Jahr', 'Kay', 'Calles', 'Fasheh', 'Vick', 'Schwartz', 'Esker', 'Cables', 'Angotti', 'Strauss', 'Justus', 'Vancamp', 'Doherty', 'Vanderpool', 'Kyle', 'Grimshaw', 'Cory', 'Keith', 'Deloatch', 'Brayton', 'Wooten', 'Holsopple', 'Garabedian', 'Gay', 'Ritter', 'Bento', 'Truxler', 'Renner', 'Hodson', 'Herbert', 'Lewter', 'Brogan', 'Marsingill', 'Wilder', 'Fujisawa', 'Klatt', 'Singletary', 'Gambill', 'Starch', 'Sandau', 'Berenbaum', 'Werner', 'Autry', 'Pickett', 'Asbury', 'Marasco', 'Benscoter', 'Vastardis', 'Hale', 'Derogatis', 'Cummings', 'Spiess', 'Deppe', 'Salo', 'Absher', 'Hendrix', 'Choate', 'Dronick', 'Elsner', 'Sinnott', 'Lira', 'Ritz', 'Pence', 'Smoot', 'Seibold', 'Lilly', 'Vega', 'Senteno', 'Sweeting', 'Chiapetti', 'Hackett', 'Ragsdale', 'Fitch', 'Duponte', 'Nieto', 'Fischl', 'Wendelin', 'Garland', 'Rogian', 'Malpass', 'Hogeland', 'Wakefield', 'Fairey', 'Sifuentes', 'Malveaux', 'Born', 'Shepherd', 'Coffell', 'Cincotta', 'Withers', 'Mack', 'Pasculli', 'Janosek', 'Spence', 'Zapata', 'Bryson', 'Uran', 'Bourgeois', 'Ferris', 'Lindberg', 'Pies', 'Ruffin', 'Maffit', 'Tagliente', 'Odom', 'Iversen', 'Nesbit', 'Fournier', 'Simon', 'Santana', 'Saxton', 'Mohan', 'Stene', 'Mccrory', 'Dietrich', 'Thackaberry', 'Alldredge', 'Ned', 'Hickox', 'Abbott', 'Crosby', 'Harp', 'Tallent', 'Andrews', 'Joy', 'Natale', 'Drey', 'Trimble', 'Hough', 'Hamelin', 'Nylen', 'Tatum', 'Komorowski', 'Bried', 'Beasley', 'Thane', 'Rossi', 'Callaway', 'Repine', 'Palomino', 'Grande', 'Bundick', 'Ruby', 'Lacy', 'Allison', 'Pettus', 'Juarez', 'Lowe', 'Post', 'Watkin', 'Milam', 'Beier', 'Shrum', 'Bradshaw', 'Tate', 'Gaytan', 'Huson', 'Costa', 'Balderas', 'Villanueva', 'Witham', 'Stelk', 'Dorais', 'Morganti', 'Lechler', 'Celedon', 'Spring', 'Alward', 'Gadwah', 'Wireman', 'Wilcher', 'Fenster', 'Christianson', 'Petaway', 'Maddy', 'Mott', 'Dresser', 'Benford', 'Zeman', 'Suehs', 'Cameron', 'Strelow', 'Thixton', 'Kluesner', 'Effinger', 'Mullaney', 'Guy', 'Gatesy', 'Hayward', 'Faust', 'Abrams', 'Davison', 'Ketterman', 'Hardin', 'Bequette', 'Habib', 'Bonilla', 'Fluty', 'Tyska', 'Trice', 'Richard', 'Earle', 'Jobst', 'Matherne', 'Barrientos', 'Spadaro', 'Gaskamp', 'Kingore', 'Hardman', 'Bundren', 'Delvalle', 'Misfeldt', 'Blough', 'Kratochvil', 'Moon', 'Sturm', 'Neumann', 'Norsworthy', 'Kieffer', 'Souza', 'Bougie', 'Buck', 'Landers', 'Monreal', 'Rivas', 'Noack', 'Macias', 'Rehl', 'Kimes', 'Durham', 'Alegre', 'Pemberton', 'Molinaro', 'Sprenger', 'Swartz', 'Mctaggart', 'Chrisman', 'Shore', 'Woody', 'Cuffie', 'Hausner', 'Thorpe', 'Eunice', 'Voris', 'Cambria', 'Arrowood', 'Larcom', 'Stamps', 'Corliss', 'Blaylock', 'Nasers', 'Holder', 'Fulbright', 'Boley', 'Mecca', 'Eurich', 'Montalbo', 'Applegate', 'Edwardson', 'Buckley', 'Quinn', 'Sorenson', 'Messana', 'Holvey', 'Holden', 'Caines', 'Downs', 'Kirkland', 'Gilmore', 'Sixon', 'Siewert', 'Albrecht', 'Digennaro', 'Levine', 'Mollette', 'Enders', 'Manzo', 'Gordon', 'Liles']
                var adjective  = ['Aristotelian', 'Arthurian', 'Bohemian', 'Brethren', 'Mosaic', 'Oceanic', 'Proctor', 'Terran', 'Tudor', 'abroad', 'absorbing', 'abstract', 'academic', 'accelerated', 'accented', 'accountant', 'acquainted', 'acute', 'addicting', 'addictive', 'adjustable', 'admired', 'adult', 'adverse', 'advised', 'aerosol', 'afraid', 'aggravated', 'aggressive', 'agreeable', 'alienate', 'aligned', 'alleged', 'almond', 'alright', 'altruistic', 'ambient', 'ambivalent', 'amiable', 'amino', 'amorphous', 'amused', 'anatomical', 'ancestral', 'angelic', 'angrier', 'answerable', 'antiquarian', 'antiretroviral', 'appellate', 'applicable', 'apportioned', 'approachable', 'appropriated', 'archer', 'aroused', 'arrested', 'assertive', 'assigned', 'athletic', 'atrocious', 'attained', 'authoritarian', 'autobiographical', 'avaricious', 'avocado', 'awake', 'awsome', 'backstage', 'backwoods', 'balding', 'bandaged', 'banded', 'banned', 'barreled', 'battle', 'beaten', 'begotten', 'beguiled', 'bellied', 'belted', 'beneficent', 'besieged', 'betting', 'biggest', 'biochemical', 'bipolar', 'blackened', 'blame', 'blessed', 'blindfolded', 'bloat', 'blocked', 'blooded', 'blushing', 'boastful', 'bolder', 'bolstered', 'bonnie', 'bored', 'boundary', 'bounded', 'bounding', 'branched', 'brawling', 'brazen', 'breeding', 'bridged', 'brimming', 'brimstone', 'broadest', 'broiled', 'broker', 'bronze', 'bruising', 'buffy', 'bullied', 'bungling', 'burial', 'buttery', 'candied', 'canonical', 'cantankerous', 'cardinal', 'carefree', 'caretaker', 'casual', 'cathartic', 'causal', 'chapel', 'characterized', 'charcoal', 'cheeky', 'cherished', 'chipotle', 'chirping', 'chivalrous', 'circumstantial', 'civic', 'civil', 'civilised', 'clanking', 'clapping', 'claptrap', 'classless', 'cleansed', 'cleric', 'cloistered', 'codified', 'colloquial', 'colour', 'combat', 'combined', 'comely', 'commissioned', 'commonplace', 'commuter', 'commuting', 'comparable', 'complementary', 'compromising', 'conceding', 'concentrated', 'conceptual', 'conditioned', 'confederate', 'confident', 'confidential', 'confining', 'confuse', 'congressional', 'consequential', 'conservative', 'constituent', 'contaminated', 'contemporaneous', 'contraceptive', 'convertible', 'convex', 'cooked', 'coronary', 'corporatist', 'correlated', 'corroborated', 'cosmic', 'cover', 'crash', 'crypto', 'culminate', 'cushioned', 'dandy', 'dashing', 'dazzled', 'decreased', 'decrepit', 'dedicated', 'defaced', 'defective', 'defenseless', 'deluded', 'deodorant', 'departed', 'depress', 'designing', 'despairing', 'destitute', 'detective', 'determined', 'devastating', 'deviant', 'devilish', 'devoted', 'diagonal', 'dictated', 'didactic', 'differentiated', 'diffused', 'dirtier', 'disabling', 'disconnected', 'discovered', 'disdainful', 'diseased', 'disfigured', 'disheartened', 'disheveled', 'disillusioned', 'disparate', 'dissident', 'doable', 'doctrinal', 'doing', 'dotted', 'downbeat', 'dozen', 'draining', 'draught', 'dread', 'dried', 'dropped', 'dulled', 'duplicate', 'eaten', 'echoing', 'economical', 'elaborated', 'elastic', 'elective', 'electoral', 'elven', 'embryo', 'emerald', 'emergency', 'emissary', 'emotional', 'employed', 'enamel', 'encased', 'encrusted', 'endangered', 'engraved', 'engrossing', 'enlarged', 'enlisted', 'enlivened', 'ensconced', 'entangled', 'enthralling', 'entire', 'envious', 'eradicated', 'eroded', 'esoteric', 'essential', 'evaporated', 'evergreen', 'everlasting', 'exacting', 'exasperated', 'excess', 'exciting', 'executable', 'existent', 'exonerated', 'exorbitant', 'exponential', 'export', 'extraordinary', 'exultant', 'exulting', 'facsimile', 'fading', 'fainter', 'fallacious', 'faltering', 'famous', 'fancier', 'fated', 'favourable', 'fearless', 'feathered', 'fellow', 'fermented', 'ferocious', 'fiddling', 'filling', 'firmer', 'fitted', 'flammable', 'flawed', 'fledgling', 'fleshy', 'flexible', 'flickering', 'floral', 'flowering', 'flowing', 'foggy', 'folic', 'foolhardy', 'foolish', 'footy', 'forehand', 'forked', 'formative', 'formulaic', 'fractional', 'fragrant', 'fraudulent', 'freakish', 'freckled', 'freelance', 'freight', 'fresh', 'fretted', 'frugal', 'fulfilling', 'fuming', 'funded', 'funny', 'garbled', 'gathered', 'geologic', 'geometric', 'gibberish', 'gilded', 'ginger', 'glare', 'glaring', 'gleaming', 'glorified', 'glorious', 'goalless', 'goody', 'grammatical', 'grande', 'grateful', 'gratuitous', 'graven', 'greener', 'grinding', 'grizzly', 'groaning', 'grudging', 'guaranteed', 'gusty', 'handheld', 'harlot', 'healing', 'healthier', 'healthiest', 'heart', 'heathen', 'hedonistic', 'heralded', 'herbal', 'hissy', 'hitless', 'holiness', 'homesick', 'honorable', 'hooded', 'hopeless', 'horrendous', 'horrible', 'huddled', 'human', 'humbling', 'humid', 'humiliating', 'hypnotized', 'idealistic', 'idiosyncratic', 'ignited', 'illustrated', 'illustrative', 'imitated', 'immense', 'immersive', 'immigrant', 'immoral', 'impassive', 'impressionable', 'improbable', 'impulsive', 'inattentive', 'inbound', 'inbounds', 'incalculable', 'incomprehensible', 'indefatigable', 'indigo', 'indiscriminate', 'indomitable', 'inert', 'inflate', 'inform', 'inheriting', 'injured', 'injurious', 'inking', 'inoffensive', 'insane', 'insensible', 'insidious', 'insincere', 'insistent', 'insolent', 'insufferable', 'intemperate', 'interdependent', 'interesting', 'interfering', 'intern', 'interpreted', 'intersecting', 'intolerable', 'intolerant', 'intuitive', 'irresolute', 'irritate', 'jealous', 'jerking', 'joining', 'joint', 'journalistic', 'joyful', 'keyed', 'knowing', 'lacklustre', 'laden', 'lagging', 'lamented', 'laughable', 'layered', 'leather', 'leathern', 'leery', 'legible', 'leisure', 'lessening', 'liberating', 'lifted', 'lightest', 'limitless', 'listening', 'literary', 'liver', 'livid', 'lobster', 'locked', 'loudest', 'loveliest', 'lowering', 'lucid', 'luckless', 'lusty', 'luxurious', 'magazine', 'maniac', 'manmade', 'maroon', 'mastered', 'mated', 'material', 'materialistic', 'meaningful', 'measuring', 'mediaeval', 'medical', 'meditated', 'medley', 'melodic', 'memorable', 'memorial', 'metabolic', 'metallic', 'metallurgical', 'metering', 'midair', 'midterm', 'midway', 'mighty', 'migrating', 'minor', 'mirrored', 'misguided', 'misshapen', 'mitigated', 'mixed', 'modernized', 'molecular', 'monarch', 'monastic', 'morbid', 'motley', 'motorized', 'mounted', 'multidisciplinary', 'muscled', 'muscular', 'muted', 'mysterious', 'mythic', 'natural', 'nauseous', 'negative', 'networked', 'neurological', 'neutered', 'newest', 'night', 'nitrous', 'noncommercial', 'nonsense', 'north', 'nuanced', 'occurring', 'offensive', 'oldest', 'oncoming', 'onstage', 'onward', 'opaque', 'operating', 'opportunist', 'opposing', 'ordinate', 'outdone', 'outlaw', 'outsized', 'overboard', 'overheated', 'oversize', 'overworked', 'oyster', 'paced', 'panting', 'paralyzed', 'paramount', 'parental', 'parted', 'partisan', 'passive', 'pastel', 'patriot', 'peacekeeping', 'pedestrian', 'peevish', 'penal', 'penned', 'pensive', 'perceptual', 'perky', 'permissible', 'pernicious', 'perpetuate', 'perplexed', 'pervasive', 'petrochemical', 'philosophical', 'picturesque', 'pillaged', 'piped', 'piquant', 'pitching', 'plausible', 'pliable', 'plumb', 'politician', 'polygamous', 'poorest', 'portmanteau', 'posed', 'positive', 'possible', 'postpartum', 'prank', 'precocious', 'predicted', 'premium', 'preparatory', 'prerequisite', 'prescient', 'preserved', 'presidential', 'pressed', 'pressurized', 'presumed', 'prewar', 'priced', 'pricier', 'primal', 'primer', 'primetime', 'printed', 'private', 'problem', 'procedural', 'process', 'prodigious', 'professional', 'programmed', 'progressive', 'prolific', 'promising', 'promulgated', 'pronged', 'proportionate', 'protracted', 'pulled', 'pulsed', 'purgatory', 'quick', 'raunchy', 'razed', 'reactive', 'readable', 'realizing', 'recognised', 'recovering', 'recurrent', 'recycled', 'redeemable', 'reflecting', 'regal', 'registering', 'reliable', 'reminiscent', 'remorseless', 'removable', 'renewable', 'repeating', 'repellent', 'reserve', 'resigned', 'respectful', 'rested', 'restrict', 'resultant', 'retaliatory', 'retiring', 'revelatory', 'reverend', 'reversing', 'revolving', 'ridiculous', 'ringed', 'risque', 'robust', 'roomful', 'rotating', 'roused', 'rubber', 'running', 'runtime', 'rustling', 'safest', 'salient', 'sanctioned', 'saute', 'saved', 'scandalized', 'scarlet', 'scattering', 'sceptical', 'scheming', 'scoundrel', 'scratched', 'scratchy', 'scrolled', 'seated', 'segregated', 'semiautomatic', 'senior', 'sensed', 'sentient', 'sexier', 'shadowy', 'shaken', 'shaker', 'shameless', 'shaped', 'shiny', 'shipped', 'shivering', 'shoestring', 'short', 'signed', 'simplest', 'simplistic', 'sizable', 'skeleton', 'skinny', 'skirting', 'skyrocketed', 'slamming', 'slanting', 'slapstick', 'sleek', 'sleepless', 'sleepy', 'slender', 'slimmer', 'smacking', 'smokeless', 'smothered', 'smouldering', 'snuff', 'socialized', 'sometime', 'sought', 'spanking', 'sparing', 'spattered', 'specialized', 'specific', 'speedy', 'spherical', 'spiky', 'spineless', 'sprung', 'squint', 'stainless', 'standing', 'starlight', 'startled', 'stately', 'statewide', 'stereoscopic', 'sticky', 'stimulant', 'stinky', 'stoked', 'stolen', 'storied', 'strained', 'strapping', 'strengthened', 'stubborn', 'stylized', 'suave', 'subjective', 'subjugated', 'subordinate', 'succeeding', 'suffering', 'summary', 'sunset', 'sunshine', 'supernatural', 'supervisory', 'surrogate', 'suspended', 'suspenseful', 'swarthy', 'sweating', 'sweeping', 'swinging', 'swooning', 'sympathize', 'synchronized', 'synonymous', 'synthetic', 'tailed', 'tallest', 'tangible', 'tanked', 'tarry', 'technical', 'tectonic', 'telepathic', 'tenderest', 'territorial', 'testimonial', 'theistic', 'thicker', 'threatening', 'timed', 'timely', 'timid', 'torrent', 'totalled', 'tougher', 'traditional', 'transformed', 'trapped', 'traveled', 'traverse', 'treated', 'trial', 'trunk', 'trusting', 'trying', 'twisted', 'tyrannical', 'unaided', 'unassisted', 'unassuming', 'unattractive', 'uncapped', 'uncomfortable', 'uncontrolled', 'uncooked', 'uncooperative', 'underground', 'undersea', 'undisturbed', 'unearthly', 'uneasy', 'unequal', 'unfazed', 'unfinished', 'unforeseen', 'unforgivable', 'unidentified', 'unimaginative', 'uninspired', 'unintended', 'uninvited', 'universal', 'unmasked', 'unorthodox', 'unparalleled', 'unpleasant', 'unprincipled', 'unread', 'unreasonable', 'unregulated', 'unreliable', 'unremitting', 'unsafe', 'unsanitary', 'unsealed', 'unsuccessful', 'unsupervised', 'untimely', 'unwary', 'unwrapped', 'uppity', 'upstart', 'useless', 'utter', 'valiant', 'valid', 'valued', 'vanilla', 'vaulting', 'vaunted', 'veering', 'vegetative', 'vented', 'verbal', 'verifying', 'veritable', 'versed', 'vinyl', 'virgin', 'visceral', 'visual', 'voluptuous', 'wanton', 'warlike', 'washed', 'waterproof', 'waved', 'weakest', 'wetting', 'wheeled', 'whirlwind', 'widen', 'widening', 'willful', 'willing', 'winnable', 'winningest', 'wireless', 'wistful', 'woeful', 'wooded', 'woodland', 'wordless', 'workable', 'worldly', 'worldwide', 'worsted', 'worthless']
                var randomname = adjective[getRandomInt(0, adjective.length + 1)] + firstnames[getRandomInt(0, firstnames.length + 1)] + surnames[getRandomInt(0, surnames.length + 1)] +getRandomInt(20, 700) +'@gmail.com'
                return randomname
            }
            

            function generategmails(){
                if (document.getElementById('loopamount').value === ''){
                    document.getElementById('loopamount').click()
                    alert('please enter an amount')
                    
                }
                else{document.getElementById('jigbutton').innerHTML = 'creating gmails'}

                

                var loopamount = parseInt(document.getElementById('loopamount').value)
                
                for (let step = 0; step < loopamount; step++) {                
                    console.log(randomname())
                    document.getElementById('newaddressbox').value += randomname() + '\\n'
                document.getElementById('jigbutton').innerHTML = 'click to generate'

                document.getElementById('clear-output').disabled = false
                document.getElementById('export').disabled = false
                }


            }
        </script>

    """
    return html_str

# class user(db.Model):
#     _tablename_ = 'userInfo'
#     KEY = db.Column(db.String,unique=True)
#     URL = db.Column(db.String,unique=True)
#     STORE = db.Column(db.String,unique=True)

# db.init_app()

def failed_template(ex):
    html_str = """
        <link rel="icon" href="https://raw.githubusercontent.com/KhushC-03/pfoliohtml/main/Novakk.png" >
        <link rel="apple-touch-icon" href="https://raw.githubusercontent.com/KhushC-03/pfoliohtml/main/Novakk.png"/>
        <body style="background-color:#030b1c"></body>
        <style>
            .QT-TEXT{
                margin: 0;
                position:fixed ;
                top: 40%;
                left: 50%;
                transform: translate(-50%, -50%);
                font-family: 'Rubik', sans-serif;
                text-transform:uppercase;
                color:red;
                font-size: 55;
                overflow: hidden;
                white-space: nowrap;
                font-weight: normal;
            }
            .redirecting{
                margin: 0;
                position:fixed ;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                font-family: 'Rubik', sans-serif;
                color:red;
                font-size: 35;
                overflow: hidden;
                white-space: nowrap;
                font-weight: normal;
            }

        </style>
        <head>
            <h1 id='qttext'  class="QT-TEXT">Cannot Start Quick Task [EXCEPTION]</h1>
            <h2 id='redirectingtext'  class="redirecting" >Redirecting In 5 Seconds...</h2>
        </head>
        <script type="text/javascript">
            function sleep (time) {
                return new Promise((resolve) => setTimeout(resolve, time));
            }
            window.onload = function getsceensize(){
                if (screen.width > 280 && screen.width < 1366){
                    document.getElementById('qttext').style = 'font-size:35;'
                    document.getElementById('redirectingtext').style = 'font-size:38;'
                    sleep(5000).then(() => {window.location.replace("http://novakk.co.uk/setkey")});
                }
                else{
                    sleep(5000).then(() => {window.location.replace("http://novakk.co.uk/setkey")});
                }
            }
        </script>
                """.replace('EXCEPTION',ex)
    return html_str

def failed_login():
    html_str = """
        <link rel="icon" href="https://raw.githubusercontent.com/KhushC-03/pfoliohtml/main/Novakk.png" >
        <link rel="apple-touch-icon" href="https://raw.githubusercontent.com/KhushC-03/pfoliohtml/main/Novakk.png"/>
        <body style="background-color:#030b1c" ></body>
        <style>
            .keybox{
                position:fixed;
                width:500px;
                left: 50%;
                height:50px;
                transform: translate(-50%, -50%);
                font-family: 'Rubik', sans-serif;
                color:#757575;
                background-color: #333f5a;
                font-size: 23;
                overflow: hidden;
                white-space: nowrap;
                font-weight: normal;
                border:none;
                text-align: center;
            }
            .keybox:hover {
                box-shadow: 0px 0px 5px 5px #8A0379;
            }
            .header{
                position:fixed;
                width:500px;
                left: 50%;
                top:20%;
                height:40px;
                transform: translate(-50%, -50%);
                font-family: 'Rubik', sans-serif;
                color:red;
                font-size: 53;
                font-weight: normal;
                border:none;
                text-align: center;        
            }
            input[type=text], textarea {
                -webkit-transition: all 0.5s ease-in-out;
                -moz-transition: all 0.5s ease-in-out;
                -ms-transition: all 0.5s ease-in-out;
                -o-transition: all 0.5s ease-in-out;
                outline: none;
                padding: 3px 0px 3px 3px;
                margin: 5px 1px 3px 0px;
                }
                
                input[type=text]:focus, textarea:focus {
            
                box-shadow: 0 0 5px #ae34db;
                padding: 3px 0px 3px 3px;
                margin: 5px 1px 3px 0px;
                border: 2px solid #ae34db;
                }

        </style>
        <head>
            <title>Novakk Login</title>
            <h1 class='header'>Invalid Credentials</h1>
        <head>
        <form action='/login' method="POST" id='loginform' name='loginform'>
            <input autocomplete="off" id='USER'name="USER" class='keybox' type='text' placeholder='License Key' value="" style="top: 50%;">
            <input autocomplete="off" id='PASSWORD'  name="PASSWORD" class='keybox' type='text' placeholder='Password' value="" style="top: 57%;">
            <input autocomplete="off" id='submit' class='keybox' type='submit' placeholder='Submit' value="Click To Login" style="top: 64.5%;">
        </form>
        <script type='text/javascript'>
            function getsceensize(){
                if (screen.width > 280 && screen.width < 1366){
                    document.getElementById('USER').style.width = 700
                    document.getElementById('PASSWORD').style.width = 700
                    document.getElementById('submit').style.width = 700      
                }
            }
            window.addEventListener("load", myInit, true); function myInit(){
                getsceensize()
            }
        </script>
                """
    return html_str

def login_template():
    html_str = """
        <link rel="icon" href="https://raw.githubusercontent.com/KhushC-03/pfoliohtml/main/Novakk.png" >
        <link rel="apple-touch-icon" href="https://raw.githubusercontent.com/KhushC-03/pfoliohtml/main/Novakk.png"/>
        <body style="background-color:#030b1c" ></body>
        <style>
            .keybox{
                position:fixed;
                min-width: 27%;
                width:auto;
                left: 50%;
                height:50px;
                transform: translate(-50%, -50%);
                font-family: 'Rubik', sans-serif;
                color:#757575;
                background-color: #333f5a;
                font-size: 23;
                overflow: hidden;
                white-space: nowrap;
                font-weight: normal;
                border:none;
                text-align: center;
                -webkit-appearance: none;
            }
            .keybox:hover {
                box-shadow: 0px 0px 5px 5px #8A0379;
            }
            input[type=text], textarea {
                -webkit-transition: all 0.5s ease-in-out;
                -moz-transition: all 0.5s ease-in-out;
                -ms-transition: all 0.5s ease-in-out;
                -o-transition: all 0.5s ease-in-out;
                outline: none;
                padding: 3px 0px 3px 3px;
                margin: 5px 1px 3px 0px;
                }
                
                input[type=text]:focus, textarea:focus {
            
                box-shadow: 0 0 5px #ae34db;
                padding: 3px 0px 3px 3px;
                margin: 5px 1px 3px 0px;
                border: 2px solid #ae34db;
            }

        </style>
        <form action='/login' method="POST" id='loginform' name='loginform'>
            <input autocomplete="off" id='USER'name="USER" class='keybox' type='text' placeholder='License Key' value="" style="top: 50%;">
            <input autocomplete="off" id='PASSWORD'  name="PASSWORD" class='keybox' type='text' placeholder='Password' value="" style="top: 57%;">
            <input autocomplete="off" id='submit' class='keybox' type='submit' placeholder='Submit' value="Click To Login" style="top: 64.5%;">
        </form>
        <script type='text/javascript'>

            function getsceensize(){
                if (screen.width > 280 && screen.width < 1366){
                    document.getElementById('USER').style.width = 700
                    document.getElementById('PASSWORD').style.width = 700
                    document.getElementById('submit').style.width = 700      
                }
            }
            window.addEventListener("load", myInit, true); function myInit(){
                getsceensize()
            }
        </script>
    """
    return html_str

def generate_nonce(length=8):
    return ''.join([str(random.randint(0, 9)) for i in range(length)])

def adminLogin(table):
    html_str = """
        <link rel="icon" href="https://raw.githubusercontent.com/KhushC-03/pfoliohtml/main/Novakk.png" >
        <link rel="apple-touch-icon" href="https://raw.githubusercontent.com/KhushC-03/pfoliohtml/main/Novakk.png"/>
        <body style="background-color:#030b1c" ></body>
        <style>
            .datatable{
                position: fixed;
                width:931px;    
                left: 28%;
                top:30%;
                overflow: auto;
                max-height: auto ;
                font-family: 'Rubik', sans-serif;
                color:#757575;
                letter-spacing:1px;
                background-color: #333f5a;
                font-size: 18;
                font-weight:lighter;
                text-align: center;
                display: inline-block;
                border-radius: 3px;
                -webkit-appearance: none;
            }
            .createkey{
                position: fixed;
                width:300;     
                left: 9%;
                overflow: auto;
                max-height: auto ;
                font-family: 'Rubik', sans-serif;
                color:#757575;
                background-color: #333f5a;
                font-size: 18;
                text-align: center;
                display: inline-block;
                border:none;
                -webkit-appearance: none;
            }
            .createkey:hover {
                box-shadow: 0px 0px 2px 2px #ae34db;
            }
            .input:hover {
                box-shadow: 0px 0px 5px 5px #ae34db;
            }
            input[type=text], textarea {
                -webkit-transition: all 0.5s ease-in-out;
                -moz-transition: all 0.5s ease-in-out;
                -ms-transition: all 0.5s ease-in-out;
                -o-transition: all 0.5s ease-in-out;
                outline: none;
                padding: 3px 0px 3px 3px;
                margin: 5px 1px 3px 0px;
                }
                
                input[type=text]:focus, textarea:focus {
            
                box-shadow: 0 0 5px #ae34db;
                padding: 3px 0px 3px 3px;
                margin: 5px 1px 3px 0px;
                border: 2px solid #ae34db;
            }

        </style>
        <table style='text-align:center' class='datatable' id='datatable'>
            <tr>
                <th style='color:white;text-align: center;padding: 0 25px;text-transform:uppercase;'>License Key</th>
                <th style='color:white;text-align: center;padding:0 25px;text-transform:uppercase;'>Store</th>
                <th style='color:white;text-align: center;padding: 0 25px;text-transform:uppercase;'>Url</th>
                <th style='color:white;text-align: center;padding: 0 25px;text-transform:uppercase;'>Bot Status</th>
            </tr>
            TABLEHERE
        
        </table>

    <input class="createkey" type='text' id='KEY' placeholder='Enter Key To Submit' value="" style="top:29.5%; height:40px"></input>
    <input class="createkey" type='submit' id='sendkey' value='Submit Key' onclick="sendKey()" style="top:35%;height:30px "></input>

    <input class="createkey" type='text' id='KEYD' placeholder='Enter Key To Deactivate' value="" style="top: 45%; height:40px"></input>
    <input class="createkey" type='submit' id='deactivatekey' value='Submit Key' onclick="deactivateKey()" style="top:50.5%;height:30px "></input>

    <input class="createkey" type='text' id='KEYF' placeholder='Enter Key To Remove' value="" style="top: 60.5%; height:40px"></input>
    <input class="createkey" type='submit' id='removekey' value='Submit Key' onclick="removeKey()" style="top:66%;height:30px "></input>
    <script>
            function setCookie(cname, cvalue, exdays) {
                const d = new Date();
                d.setTime(d.getTime() + (exdays*24*60*60*1000));
                let expires = "expires="+ d.toUTCString();
                var cook = document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
                console.log(cook)
            }
            function makeid(length) {
                var result = '';
                var characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
                var charactersLength = characters.length;
                for ( var i = 0; i < length; i++ ) {
                result += characters.charAt(Math.floor(Math.random() * 
            charactersLength));
            }
            return result;
            }
            
            function sendKey(){
                FOUNDKEY = document.getElementById('KEY').value
                if (FOUNDKEY == ''){FOUNDKEY = `NVK-${makeid(16)}`}
                fetch(`http://novakk.co.uk/addkey?KEY=${FOUNDKEY}`, {
                    method: 'GET',
                }).then(response => response.json())
                .then(fetchresponse => {
                if(fetchresponse.message == 'success'){
                    if (screen.width > 280 && screen.width < 1366){
                        location.reload();
                        window.addEventListener("load", myInit, true); function myInit(){
                            document.getElementById('KEY').value = `SUCCESS ${FOUNDKEY}`
                            document.getElementById('KEY').style = `color:#757575; top:42%; height:55px; width:700; left: 14%;`
                        }
                        
                    }
                    else{
                        location.reload();
                        window.addEventListener("load", myInit, true); function myInit(){
                            document.getElementById('KEY').value = `SUCCESS ${FOUNDKEY}`
                            document.getElementById('KEY').style = `color:#757575; top:29.5%; height:40px`  
                        }
                    }
                
                }
                else{
                    if (screen.width > 280 && screen.width < 1366){
                        document.getElementById('KEY').value = `ERROR ${FOUNDKEY}`
                        document.getElementById('KEY').style = `color:red; top:42%; height:55px; width:700; left: 14%;`
                    }
                    else{
                        document.getElementById('KEY').value = `ERROR ${FOUNDKEY}`
                        document.getElementById('KEY').style = `color:red; top:29.5%; height:40px`                
                    }
                }
                }
                )
            }
            function deactivateKey(){
                FOUNDKEY = document.getElementById('KEYD').value
                fetch(`http://novakk.co.uk/deactivate?KEY=${FOUNDKEY}`, {
                    method: 'GET',
                }).then(response => response.json())
                .then(fetchresponse => {
                if(fetchresponse.message == 'success'){
                    if (screen.width > 280 && screen.width < 1366){
                        location.reload();
                        window.addEventListener("load", myInit, true); function myInit(){
                            document.getElementById('KEYD').value = `SUCCESS ${FOUNDKEY}`;
                            document.getElementById('KEYD').style = `color:#757575; top:52%; height:55px; width:700; left: 14%;`;
                        }
                    }else{
                        location.reload();
                        window.addEventListener("load", myInit, true); function myInit(){
                            document.getElementById('KEYD').value = `SUCCESS ${FOUNDKEY}`;
                            document.getElementById('KEYD').style = `color:#757575; top: 45%; height:40px`;
                        }
                    }
                    }
                else{
                    if (screen.width > 280 && screen.width < 1366){
                        document.getElementById('KEYD').value = `ERROR ${FOUNDKEY}`;
                        document.getElementById('KEYD').style = `color:red; top:52%; height:55px; width:700; left: 14%;`;
                    }
                    else{
                        document.getElementById('KEYD').value = `ERROR ${FOUNDKEY}`;
                        document.getElementById('KEYD').style = `color:red; top: 45%; height:40px`;
                    }
                }}
                )
            }
            function removeKey(){
                FOUNDKEY = document.getElementById('KEYF').value
                fetch(`http://novakk.co.uk/remove?KEY=${FOUNDKEY}`, {
                    method: 'GET',
                }).then(response => response.json())
                .then(fetchresponse => {
                if(fetchresponse.message == 'success'){
                    if (screen.width > 280 && screen.width < 1366){
                        location.reload();
                        window.addEventListener("load", myInit, true); function myInit(){
                            document.getElementById('KEYF').value = `SUCCESS ${FOUNDKEY}`;
                            document.getElementById('KEYF').style = `color:#757575; top:62%; height:55px; width:700; left: 14%;`;
                        }

                    }else{
                        location.reload();
                        window.addEventListener("load", myInit, true); function myInit(){
                            document.getElementById('KEYF').value = `SUCCESS ${FOUNDKEY}`;
                            document.getElementById('KEYF').style = `color:#757575; top: 45%; height:40px`;
                        }
                    }
                    }
                else{
                    if (screen.width > 280 && screen.width < 1366){
                        document.getElementById('KEYF').value = `ERROR ${FOUNDKEY}`;
                        document.getElementById('KEYF').style = `color:red; top:62%; height:55px; width:700; left: 14%;`;
                    }
                    else{
                        document.getElementById('KEYF').value = `ERROR ${FOUNDKEY}`;
                        document.getElementById('KEYF').style = `color:red; top: 45%; height:40px`;
                    }
                }}
                )
            }
            function getsceensize(){
                if (screen.width > 280 && screen.width < 1366){
                    document.getElementById('KEY').style ='top:42%; height:55px; width:700; left: 14%;'
                    document.getElementById('sendkey').style ='top:46.5%; height:55px; width:700; left: 14%;'
                    document.getElementById('KEYD').style ='top:52%; height:55px; width:700; left: 14%;'
                    document.getElementById('deactivatekey').style ='top:56.5%; height:55px; width:700; left: 14%;'

                    document.getElementById('KEYF').style ='top:62%; height:55px; width:700; left: 14%;'
                    document.getElementById('removekey').style ='top:66.5%; height:55px; width:700; left: 14%;'


                    document.getElementById('datatable').style ='top:20%; left: 4%; width:900px; text-align:center;'
                    
                }
            }
            window.addEventListener("load", myInit, true); function myInit(){
                setCookie('LOGIN', 'True', 10000)
                getsceensize()
            }
    </script>
    """.replace('TABLEHERE',table)
    return html_str

def downloadpage(ex):
    if ex == True:
        html_str = """
        <link rel="apple-touch-icon" href="https://raw.githubusercontent.com/KhushC-03/pfoliohtml/main/Novakk.png"/>
        <link rel="icon" href="https://raw.githubusercontent.com/KhushC-03/pfoliohtml/main/Novakk.png" >
        <body style="background-color:#030b1c" ></body>
        <style>
            .keybox{
                position:fixed ;
                top: 50%;
                min-width: 27%;
                width:auto;
                left: 50%;
                height:5%;
                transform: translate(-50%, -50%);
                font-family: 'Rubik', sans-serif;
                color:#ffffff;
                background-color: #333f5a;
                font-size: 23;
                overflow: hidden;
                white-space: nowrap;
                font-weight: normal;
                border:none;
                text-align: center;
                -webkit-appearance: none;
            }
            .manualqt{
                position:fixed ;
                min-width: 27%;
                width:auto;
                left: 50%;
                height:5%;
                transform: translate(-50%, -50%);
                font-family: 'Rubik', sans-serif;
                color:#ffffff;
                background-color: #333f5a;
                font-size: 23;
                overflow: hidden;
                white-space: nowrap;
                font-weight: normal;
                border:none;
                opacity: 100%;


                -webkit-appearance: none;
            }
            h1{
                position:fixed ;
                min-width: 27%;
                width:auto;
                top: 30.5%;
                left: 50%;
                transform: translate(-50%, -50%);
                font-family: 'Rubik', sans-serif;
                color:red;
                font-size: 43;
                overflow: hidden;
                white-space: nowrap;
                font-weight: normal;
                border:none;
                opacity: 100%;
                text-align:center;

                -webkit-appearance: none;        
            }

            #wrapper>div {
                display: inline-block;
                margin: auto;
                text-align: left;
            }
            #wrapper>div:first-child {
                width: 15%;
            }
            #wrapper>div:nth-child(2) {
                width: 56%; /* or less */
            }
            #wrapper>div:last-child {
                width: 25%;
            }
            input[type=text], textarea {
                -webkit-transition: all 0.5s ease-in-out;
                -moz-transition: all 0.5s ease-in-out;
                -ms-transition: all 0.5s ease-in-out;
                -o-transition: all 0.5s ease-in-out;
                outline: none;
                padding: 3px 0px 3px 3px;
                margin: 5px 1px 3px 0px;
                }
                
            input[type=text]:focus, textarea:focus {
            
                box-shadow: 0 0 5px #ae34db;
                padding: 3px 0px 3px 3px;
                margin: 5px 1px 3px 0px;
                border: 2px solid #ae34db;
            }
            #store{
                display:flex;
                justify-content:center;
            }   

            
        </style>

        ERROR HERE

        <form action='/download' method='POST'>
            <input autocomplete="off" id="keybox" name='KEY' class='keybox' style="text-align: center; "type='text' placeholder='Please Enter Your Licence Key Here' value="" >
            <input  class='manualqt' id='qtstart' type="submit" value="Click To Download" placeholder="Click To Download" style='top: 60.5%;'>
        </form>




        <script type='text/javascript'>
            function getsceensize(){
                if (screen.width > 280 && screen.width < 1366){
                    document.getElementById('qtstart').style.width = 700      
                    document.getElementById('keybox').style.width = 700  
                }
            }
            window.addEventListener("load", myInit, true); function myInit(){getsceensize()}
        </script>
        """.replace('ERROR HERE','<h1>Key Could Not Be Found</h1>')
        return html_str
    else:
        html_str = """
        <body style="background-color:#030b1c" ></body>
        <link rel="apple-touch-icon" href="https://raw.githubusercontent.com/KhushC-03/pfoliohtml/main/Novakk.png"/>
        <link rel="icon" href="https://raw.githubusercontent.com/KhushC-03/pfoliohtml/main/Novakk.png" >
        <style>
            .keybox{
                position:fixed ;
                top: 50%;
                min-width: 27%;
                width:auto;
                left: 50%;
                height:5%;
                transform: translate(-50%, -50%);
                font-family: 'Rubik', sans-serif;
                color:#ffffff;
                background-color: #333f5a;
                font-size: 23;
                overflow: hidden;
                white-space: nowrap;
                font-weight: normal;
                border:none;
                text-align: center;
                -webkit-appearance: none;
            }
            .manualqt{
                position:fixed ;
                min-width: 27%;
                width:auto;
                left: 50%;
                height:5%;
                transform: translate(-50%, -50%);
                font-family: 'Rubik', sans-serif;
                color:#ffffff;
                background-color: #333f5a;
                font-size: 23;
                overflow: hidden;
                white-space: nowrap;
                font-weight: normal;
                border:none;
                opacity: 100%;


                -webkit-appearance: none;
            }


            #wrapper>div {
                display: inline-block;
                margin: auto;
                text-align: left;
            }
            #wrapper>div:first-child {
                width: 15%;
            }
            #wrapper>div:nth-child(2) {
                width: 56%; /* or less */
            }
            #wrapper>div:last-child {
                width: 25%;
            }
            input[type=text], textarea {
                -webkit-transition: all 0.5s ease-in-out;
                -moz-transition: all 0.5s ease-in-out;
                -ms-transition: all 0.5s ease-in-out;
                -o-transition: all 0.5s ease-in-out;
                outline: none;
                padding: 3px 0px 3px 3px;
                margin: 5px 1px 3px 0px;
                }
                
            input[type=text]:focus, textarea:focus {
            
                box-shadow: 0 0 5px #ae34db;
                padding: 3px 0px 3px 3px;
                margin: 5px 1px 3px 0px;
                border: 2px solid #ae34db;
            }
            #store{
                display:flex;
                justify-content:center;
            }   

            
        </style>


        <form action='/download' method='POST'>
            <input autocomplete="off" id="keybox" name='KEY' class='keybox' style="text-align: center; "type='text' placeholder='Please Enter Your Licence Key Here' value="" >
            <input  class='manualqt' id='qtstart' type="submit" value="Click To Download" placeholder="Click To Download" style='top: 60.5%;'>
        </form>




        <script type='text/javascript'>
            function getsceensize(){
                if (screen.width > 280 && screen.width < 1366){
                    document.getElementById('qtstart').style.width = 700      
                    document.getElementById('keybox').style.width = 700  
                }
            }
            window.addEventListener("load", myInit, true); function myInit(){getsceensize()}
        </script>
        """
        return html_str

def uploadoage():
    html_str = """"
        <body style="background-color:#030b1c" ></body>
        <link rel="apple-touch-icon" href="https://raw.githubusercontent.com/KhushC-03/pfoliohtml/main/Novakk.png"/>
        <link rel="icon" href="https://raw.githubusercontent.com/KhushC-03/pfoliohtml/main/Novakk.png" >
        <style>
            .filebox{
                position:fixed ;
                top: 50%;
                min-width: 27%;
                width:auto;
                left: 50%;
                height:5%;
                transform: translate(-50%, -50%);
                font-family: 'Rubik', sans-serif;
                color:#ffffff;
                background-color: #333f5a;
                font-size: 23;
                overflow: hidden;
                white-space: nowrap;
                font-weight: normal;
                border:none;
                text-align: center;
                
            }
            .filesubmit{
                position:fixed ;
                min-width: 27%;
                width:auto;
                left: 50%;
                height:5%;
                transform: translate(-50%, -50%);
                font-family: 'Rubik', sans-serif;
                color:#ffffff;
                background-color: #333f5a;
                font-size: 23;
                overflow: hidden;
                white-space: nowrap;
                font-weight: normal;
                border:none;
                opacity: 100%;
            }
            h1{
                position:fixed ;
                min-width: 27%;
                width:auto;
                top: 30.5%;
                left: 50%;
                transform: translate(-50%, -50%);
                font-family: 'Rubik', sans-serif;
                color:white;
                font-size: 43;
                overflow: hidden;
                white-space: nowrap;
                font-weight: normal;
                border:none;
                opacity: 100%;
                text-align:center;
            }

            #wrapper>div {
                display: inline-block;
                margin: auto;
                text-align: left;
            }
            #wrapper>div:first-child {
                width: 15%;
            }
            #wrapper>div:nth-child(2) {
                width: 56%; /* or less */
            }
            #wrapper>div:last-child {
                width: 25%;
            }
            input[type=text], textarea {
                -webkit-transition: all 0.5s ease-in-out;
                -moz-transition: all 0.5s ease-in-out;
                -ms-transition: all 0.5s ease-in-out;
                -o-transition: all 0.5s ease-in-out;
                outline: none;
                padding: 3px 0px 3px 3px;
                margin: 5px 1px 3px 0px;
                }
                
            input[type=text]:focus, textarea:focus {
            
                box-shadow: 0 0 5px #ae34db;
                padding: 3px 0px 3px 3px;
                margin: 5px 1px 3px 0px;
                border: 2px solid #ae34db;
            }
            #store{
                display:flex;
                justify-content:center;
            }   

            
        </style>

        <h1>Upload File</h1>

        <input  class='filebox' id='fileholder'type='button' value="Please Select You File Here" placeholder='Please Select You File Here' onclick="clickfile()">
        <form action='/upload' method='POST' enctype="multipart/form-data">
            <input  id="version" type='text' name='version' class='filebox' placeholder='Input File Version' value="" style='top: 55.5%;'>
            <input  id="filebox" type='file' name='filebox' class='filebox' placeholder='Please Select You File Here' value="" style="visibility:hidden;">
            <input  class='filesubmit' id='filesubmit' type="submit" value="Submit File" placeholder="Submit File" style='top: 62%;'>
        </form>
        <script type='text/javascript'>
            function chnagefile(){
                if (document.getElementById('filebox').value==""){}
                else{document.getElementById('fileholder').value= document.getElementById("filebox").files[0].name}
            }
            function clickfile(){
                document.getElementById('filebox').click()
                window.setInterval(function(){chnagefile()}, 1000)
            }
            function getsceensize(){
                if (screen.width > 280 && screen.width < 1366){
                    document.getElementById('filebox').style.width = 700      
                    document.getElementById('filesubmit').style.width = 700  
                }
            }
            window.addEventListener("load", myInit, true); function myInit(){getsceensize()}
        </script>
        """
    return html_str

def submitform():
    html_str = """
        <link rel="apple-touch-icon" href="https://raw.githubusercontent.com/KhushC-03/pfoliohtml/main/Novakk.png"/>
        <link rel="icon" href="https://raw.githubusercontent.com/KhushC-03/pfoliohtml/main/Novakk.png" >
        <meta charset='utf-8'>
        <meta  name='viewport' content='width=device-width, initial-scale=1, shrink-to-fit=no'>
        <body style="background-color:black">



        <style>

            p {
                white-space: nowrap;
                overflow: hidden;
                font-size:45px;
                position: fixed;
                left: 50%;
                top:400px;
                color:white;
                font-family: 'Rubik', sans-serif;
                transform: translate(-50%, -50%);
                height:50%;
                text-transform:uppercase;
                letter-spacing:7px;
                -webkit-appearance: none;
            }
        </style>


        <p id="welcome">Thank You</p >
    """
    return html_str

@app.route('/getnovakkvisitorscount',methods=['GET'])
def get_visitor_count():
    GETALLINFO = engine.execute("""
    SELECT ALL GEODATA, REQID FROM visitors;""").fetchall()
    parsedData = []
    timestamps = []
    for e in GETALLINFO:
        try:
            parsedData.append([{'metadata':json.loads(e[0])}])
            timestamps.append(e[1])
        except:
            pass
    return jsonify({"message":"success",'last time':timestamps[len(timestamps)-1],"visitor count":len(timestamps),'last visitor data':parsedData[len(parsedData)-1]})  

@app.route('/')
def home():
    html_str = """
        <link rel="icon" href="https://raw.githubusercontent.com/KhushC-03/pfoliohtml/main/Novakk.png" >
        <meta charset='utf-8'>
        <meta  name='viewport' content='width=device-width, initial-scale=1, shrink-to-fit=no'>
        <body style="background-color:black">
        <html lang='en' ></html>

        <style>
            body {
                margin:0;
                padding:0;
                background:black;
                color:white;
                font-family: 'Rubik', sans-serif;
                
            }
            p {
                white-space: nowrap;
                overflow: hidden;
                font-size:50px;
                position: fixed;
                left: 50%;
                top:400px;
                transform: translate(-50%, -50%);
                height:100px;
                text-transform:uppercase;
                letter-spacing:10px;
                -webkit-appearance: none;
            }
        </style>


        <p id="welcome" style="visibility: visible">Welcome To Novakk</p >


        <script type='text/javascript'>
            function setCookie(cname, cvalue, exdays) {
            const d = new Date();
            d.setTime(d.getTime() + (exdays*24*60*60*1000));
            let expires = "expires="+ d.toUTCString();
            var cook = document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
            console.log(cook)
            }
            function fadeOut(element) {
            var op = 1;  // initial opacity
            var timer = setInterval(function () {
                if (op <= 0.1){
                    clearInterval(timer);
                }
                element.style.opacity = op;
                op -= 0.1;
                }, 50);
            }
            function fadeIn(el) {
            el.style.opacity = 0;
            var tick = function () {
                el.style.opacity = +el.style.opacity + 0.01;
                if (+el.style.opacity < 1) {
                    (window.requestAnimationFrame && requestAnimationFrame(tick)) || setTimeout(tick, 16)
                }
            };
            tick();
            }
            function sleep (time) {
            return new Promise((resolve) => setTimeout(resolve, time));
            }
            function rand(min, max) {
                return Math.floor(Math.random() * (max - min + 1)) + min;
            }
            function getRandomLetter() {
                var alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
                return alphabet[rand(0, alphabet.length - 1)]
            }
            function getRandomWord(word) {
                var text = word.innerHTML
                var finalWord = ''
                for (var i = 0; i < text.length; i++) {
                    finalWord += text[i] == ' ' ? ' ' : getRandomLetter()
                }     
                return finalWord      
            }

            var word = document.querySelector('p')
            var interv = 'undefined'
            var canChange = false
            var globalCount = 0
            var count = 0
            var INITIAL_WORD = word.innerHTML;
            var isGoing = false

            function init() {
                if (isGoing) return;
                isGoing = true
                var randomWord = getRandomWord(word)
                word.innerHTML = randomWord
                interv = setInterval(function() {         
                    var finalWord = ''
                    for (var x = 0; x < INITIAL_WORD.length; x++) {
                        if (x <= count && canChange) {
                            finalWord += INITIAL_WORD[x]
                        } else {
                            finalWord += getRandomLetter()
                        }
                    }
                    word.innerHTML = finalWord
                    if (canChange) {
                        count++
                    }
                    if (globalCount >= 20) {
                        canChange = true             
                    }
                    if (count >= INITIAL_WORD.length) {
                        clearInterval(interv)
                        count = 0
                        canChange = false
                        globalCount = 0
                        isGoing = false
                        sleep(1200).then(() => {
                        fadeOut(document.getElementById("welcome"));
                        });
                        sleep(1600).then(() => {
                        fadeIn(document.querySelector(".MainTitle"));
                        fadeIn(document.querySelector(".MainImage"));
                        fadeIn(document.querySelector(".software-span"));  
                        });
                        sleep(1800).then(() => {fadeIn(document.querySelector(".intrest-button"));});
                        sleep(2300).then(() => {
                        fadeIn(document.querySelector(".interest-form"));
                        fadeIn(document.querySelectorAll(".social-image")[0]);
                        fadeIn(document.querySelectorAll(".social-image")[1]);
                        });
                        
                        //sleep(2500).then(() => {fadeIn(document.querySelector(".interest-form"));  });
                    }
                    globalCount++
                }, 50)
            }
            window.onload = function main(){
            if (screen.width > 500 && screen.width < 1050){
                document.getElementById('mainImage').height = 380
                document.getElementById('welcome').style = 'font-size: 45px; top:25%; letter-spacing:5px;'
                document.querySelector('.software-span').style = 'font-size:27px; letter-spacing:3px; top:45%;'
                document.getElementById('container').style = 'top:27%;'
                document.querySelector('.intrest-button').style = 'font-size:25px; top:49%; letter-spacing:3px;'
                document.querySelector('.interest-form').style = 'top:53%;'
                document.querySelectorAll('.inputFields')[0].style = "font-size:15px; color:white; width: 120px; background-color: #000000; font-family: 'Rubik', sans-serif; border:none;"
                document.querySelectorAll('.inputFields')[1].style = "font-size:15px; color:white; width: 120px; background-color: #000000; font-family: 'Rubik', sans-serif; border:none;"
                document.querySelectorAll('.inputFields')[2].style = "font-size:15px; color:white; width: 160px; background-color: #000000; font-family: 'Rubik', sans-serif; border:none;"
                document.querySelectorAll('.inputFields')[3].style = "font-size:15px; color:white; width: 85px; background-color: #000000; font-family: 'Rubik', sans-serif; border:none;"
                document.querySelectorAll('.social-image')[0].style = 'top:54%; left:47.5%'
                document.querySelectorAll('.social-image')[1].style = 'top:54%; left:49.5%'
                document.querySelectorAll('.social-image')[0].height = 19
                document.querySelectorAll('.social-image')[1].height = 19
                document.querySelectorAll('.social-image')[0].width = 19
                document.querySelectorAll('.social-image')[1].width = 19
            }
            if (screen.width > 399 && screen.width < 499){
                document.getElementById('mainImage').height = 160
                document.getElementById('welcome').style = 'font-size: 19px; top:25%; letter-spacing:5px;'
                document.querySelector('.software-span').style = 'font-size:9px; letter-spacing:3px; top:47%;'
                document.getElementById('container').style = 'top:27%;'
                document.querySelector('.intrest-button').style = 'font-size:9px; top:51%; letter-spacing:3px;'
                document.querySelector('.interest-form').style = 'top:55%;'
                document.querySelectorAll('.inputFields')[0].style = "font-size:7px; color:white; width: 50px; background-color: #000000; font-family: 'Rubik', sans-serif; border:none;"
                document.querySelectorAll('.inputFields')[1].style = "font-size:7px; color:white; width: 50px; background-color: #000000; font-family: 'Rubik', sans-serif; border:none;"
                document.querySelectorAll('.inputFields')[2].style = "font-size:7px; color:white; width: 80px; background-color: #000000; font-family: 'Rubik', sans-serif; border:none;"
                document.querySelectorAll('.inputFields')[3].style = "font-size:7px; color:white; width: 50px; background-color: #000000; font-family: 'Rubik', sans-serif; border:none;"
                document.querySelectorAll('.social-image')[0].style = 'top:56%; left:47.5%'
                document.querySelectorAll('.social-image')[1].style = 'top:56%; left:49.5%'
                document.querySelectorAll('.social-image')[0].height = 10
                document.querySelectorAll('.social-image')[1].height = 10
                document.querySelectorAll('.social-image')[0].width = 10
                document.querySelectorAll('.social-image')[1].width = 10
            }
            if (screen.width > 350 && screen.width < 399){
                document.getElementById('mainImage').height = 160
                document.getElementById('welcome').style = 'font-size: 19px; top:25%; letter-spacing:5px;'
                document.querySelector('.software-span').style = 'font-size:9px; letter-spacing:3px; top:43%;'
                document.getElementById('container').style = 'top:27%;'
                document.querySelector('.intrest-button').style = 'font-size:9px; top:46%; letter-spacing:3px;'
                document.querySelector('.interest-form').style = 'top:50%;'
                document.querySelectorAll('.inputFields')[0].style = "font-size:7px; color:white; width: 50px; background-color: #000000; font-family: 'Rubik', sans-serif; border:none;"
                document.querySelectorAll('.inputFields')[1].style = "font-size:7px; color:white; width: 50px; background-color: #000000; font-family: 'Rubik', sans-serif; border:none;"
                document.querySelectorAll('.inputFields')[2].style = "font-size:7px; color:white; width: 80px; background-color: #000000; font-family: 'Rubik', sans-serif; border:none;"
                document.querySelectorAll('.inputFields')[3].style = "font-size:7px; color:white; width: 50px; background-color: #000000; font-family: 'Rubik', sans-serif; border:none;"
                document.querySelectorAll('.social-image')[0].style = 'top:51%; left:47.5%'
                document.querySelectorAll('.social-image')[1].style = 'top:51%; left:49.5%'
                document.querySelectorAll('.social-image')[0].height = 10
                document.querySelectorAll('.social-image')[1].height = 10
                document.querySelectorAll('.social-image')[0].width = 10
                document.querySelectorAll('.social-image')[1].width = 10
            }
            if (screen.width > 280 && screen.width < 349){
                document.getElementById('mainImage').height = 110
                document.getElementById('welcome').style = 'font-size: 12px; top:25%; letter-spacing:5px;'
                document.querySelector('.software-span').style = 'font-size:7px; letter-spacing:3px; top:41%;'
                document.getElementById('container').style = 'top:27%;'
                document.querySelector('.intrest-button').style = 'font-size:7px; top:44%; letter-spacing:3px;'
                document.querySelector('.interest-form').style = 'top:48%;'
                document.querySelectorAll('.inputFields')[0].style = "font-size:5px; color:white; width: 40px; background-color: #000000; font-family: 'Rubik', sans-serif; border:none;"
                document.querySelectorAll('.inputFields')[1].style = "font-size:5px; color:white; width: 40px; background-color: #000000; font-family: 'Rubik', sans-serif; border:none;"
                document.querySelectorAll('.inputFields')[2].style = "font-size:5px; color:white; width: 60px; background-color: #000000; font-family: 'Rubik', sans-serif; border:none;"
                document.querySelectorAll('.inputFields')[3].style = "font-size:5px; color:white; width: 40px; background-color: #000000; font-family: 'Rubik', sans-serif; border:none;"
                document.querySelectorAll('.social-image')[0].style = 'top:49%; left:47.5%'
                document.querySelectorAll('.social-image')[1].style = 'top:49%; left:49.5%'
                document.querySelectorAll('.social-image')[0].height = 10
                document.querySelectorAll('.social-image')[1].height = 10
                document.querySelectorAll('.social-image')[0].width = 10
                document.querySelectorAll('.social-image')[1].width = 10
            }
            init()
            }
            //function showform(){window.open('https://docs.google.com/forms/d/e/1FAIpQLSdSx6yTIuxLt4VVUurXvnsIEccE97Tdfu0XM7FKaty9W6biVw/viewform?')}

            function checkform(){
            var Name = document.getElementById('Name').value;
            var Discord = document.getElementById('Discord').value;
            var email = document.getElementById('Email').value;
            if (Name.length > 0){
            }
            else{
                alert('Please Enter An Name')
                return false;
            }
            if (Discord.length > 0){
            }
            else{
                alert('Please Enter A Discord ID')
                return false;
            }
            if (email.length > 0){
            }
            else{
                alert('Please Enter An Email')
                return false;
            }
            }
            function loadInsta(){
                window.open('https://www.instagram.com/khush_chauh4n/')
            }
            function loadTwitter(){
                window.open('https://twitter.com/KhushChauhan5')
            }

        </script>



        <style>
            .MainTitle{
                color: #8A0379;
                position: absolute;
                left: 50%;
                transform: translate(-50%, -50%);
                filter: brightness(120%);
                top: 98px;
                opacity: 0%;
                font-size: 25px;
                text-shadow: 0.5px 0.5px 1px black, 0 0 28px #8A0379, 0 0 6px #8A0379;
                -webkit-appearance: none;
            }
            .intrest-button{
                color:white;
                font-family: 'Rubik', sans-serif;
                text-transform:uppercase;
                letter-spacing:10px;
                border:none;
                background-color:black;
                white-space: nowrap;
                overflow: hidden;
                font-size:20px;
                position: absolute;
                left: 50%;
                top:760px;
                opacity: 0%;
                transform: translate(-50%, -50%);    
                transition: all 0.2s ease-in-out;
                border-radius: none;
                -webkit-appearance: none;
            }
            #container {
                background-color:black;
                position: absolute;
                left: 50%;
                top:450px;
                transform: translate(-50%, -50%);
            }
            .MainImage {
                border-radius: 8px;
                box-shadow: 0px 0px 10px 10px #8A0379;
                position: fixed;
                opacity: 0%
            }

            .inputFields:hover {
                box-shadow:  0px 0px 5px 5px #8A0379;
            }
            .inputFields{
                -webkit-appearance: none;
            }
            .interest-form {
                color:white;
                white-space: nowrap;
                font-size:20px;
                position: absolute;
                left: 50%;
                top:810px;
                opacity: 0%;
                transform: translate(-50%, -50%);    
                transition: all 0.2s ease-in-out;
                border-radius: none;
                -webkit-appearance: none;
            }
            .software-span {
                color:white;
                font-family: 'Rubik', sans-serif;
                text-transform:uppercase;
                letter-spacing:6px;
                border:none;
                background-color:black;
                white-space: nowrap;
                overflow: hidden;
                font-size:20px;
                position: absolute;
                left: 50%;
                top:720px;
                opacity: 0%;
                transform: translate(-50%, -50%);    
                transition: all 0.2s ease-in-out;
                border-radius: none;
                -webkit-appearance: none;
            }
            .footer-span {
                color:white;
                font-family: 'Rubik', sans-serif;
                letter-spacing:3px;
                border:none;
                background-color:black;
                white-space: nowrap;
                overflow: hidden;
                font-size:20px;
                position: absolute;
                left: 50%;
                top:870px;
                opacity: 0%;
                transition: all 0.2s ease-in-out;
                border-radius: none;
                -webkit-appearance: none;
            }
            .social-image {
                border:none;
                background-color:black;
                white-space: nowrap;
                overflow: hidden;
                position: absolute;
                left: 50%;
                top:950px;
                opacity: 0%;    
                transition: all 0.2s ease-in-out;
                border-radius: none;
                -webkit-appearance: none;
            }
            ::placeholder { /* Chrome, Firefox, Opera, Safari 10.1+ */
                color: white;
            }
            input[type=text], textarea {
                -webkit-transition: all 0.3s ease-in-out;
                -moz-transition: all 0.3s ease-in-out;
                -ms-transition: all 0.3s ease-in-out;
                -o-transition: all 0.3s ease-in-out;
                outline: none;
                padding: 5px 0px 5px 5px;
                margin: 5px 1px 5px 0px;
                }
                
            input[type=text]:focus, textarea:focus {

                box-shadow: 0 0 14px #8A0379;
                padding: 5px 5px 5px 5px;
                margin: 5px 5px 5px 5px;
                border: 5px solid #8A0379;
            }
            input[type=submit], textarea {
                -webkit-transition: all 0.3s ease-in-out;
                -moz-transition: all 0.3s ease-in-out;
                -ms-transition: all 0.3s ease-in-out;
                -o-transition: all 0.3s ease-in-out;
                outline: none;
                padding: 3px 0px 3px 3px;
                margin: 5px 1px 3px 0px;
                }
                
            input[type=submit]:focus, textarea:focus {
                box-shadow: 0 0 7px #8A0379;
                padding: 3px 3px 3px 3px;
                margin: 5px 3px 3px 0px;
                border: 3px solid #8A0379;
            }
        </style>





        <head>
        <title>Novakk</title>


        <h1 class="MainTitle" id='mainsection' >
        </h1>
        <div id='container' class="MainImage" >
            <img alt="novakk cli" src="https://raw.githubusercontent.com/KhushC-03/pfoliohtml/main/Novakk%20MAIN.png" height='453' id='mainImage' >
        </div>
        <div><span class='software-span'>Software Automation Done Right.</span></div> 
        <span  class='intrest-button'> Show Interest</span>
        <img alt="instagram icon" class='social-image' src="https://raw.githubusercontent.com/KhushC-03/pfoliohtml/main/instagram.png" height='18' width='18'  style="left: 47.5%; top:825px;" onclick='loadInsta()'>
        <img alt="twitter icon" class='social-image' src="https://raw.githubusercontent.com/KhushC-03/pfoliohtml/main/twitter.png" height='18' width='18'  style="left:49.5%; top:825px;" onclick="loadTwitter()">
        </head>

        <div class="interest-form">
        <form action='/ShowInterestForm' onsubmit='return checkform()' method="POST" class="signupForm" name="signupform" autocomplete="off" >
            <input type="text" class="inputFields"  id="Name" name="Name" placeholder="Full Name" value="" style="letter-spacing:1px; color:white; width: 150px; background-color: #000000; font-family: 'Rubik', sans-serif; border:none;"/>
            <input type="text" class="inputFields"  id="Discord" name="Discord" placeholder="Discord ID" value="" style="letter-spacing:1px; color:white; width: 150px; background-color: #000000; font-family: 'Rubik', sans-serif; border:none;"/>
            <input type="text" class="inputFields"  id="Email" name="Email" placeholder="Email Address" value="" style="letter-spacing:1px; color:white; width: 220px; background-color: #000000; font-family: 'Rubik', sans-serif; border:none;"/>
            <input type="submit"class='inputFields' id="join-btn" name="Submit" value="Submit " style="letter-spacing:1px; color:white; background-color: #000000; font-family: 'Rubik', sans-serif; border:none;">
        </form>
        </div>







    
    """
    # geoip_data = json.dumps(simple_geoip.get_geoip_data())
    # REQID = generate_nonce(length=8)
    # time = datetime.now()

    # engine.execute(
    #     f"""
    # INSERT INTO visitors (GEODATA, REQID)
    # VALUES ('{geoip_data}', '{time}');
    # """)
    return render_template_string(html_str)

@app.route('/setkey')
def setkey():
    html_str = """   
        <link rel="icon" href="https://raw.githubusercontent.com/KhushC-03/pfoliohtml/main/Novakk.png" >
        <link rel="apple-touch-icon" href="https://raw.githubusercontent.com/KhushC-03/pfoliohtml/main/Novakk.png"/>
        <body style="background-color:#000000" ></body>
        <style>
            .keybox{
                position:fixed ;
                top: 50%;
                min-width: 27%;
                width:auto;
                left: 50%;
                height:5%;
                transform: translate(-50%, -50%);
                font-family: 'Rubik', sans-serif;
                color:#ffffff;
                background-color: #313131;
                font-size: 23;
                overflow: hidden;
                white-space: nowrap;
                font-weight: normal;
                border:none;
                text-align: center;
                -webkit-appearance: none;
            }
            .manualqt{
                position:fixed ;
                min-width: 27%;
                width:auto;
                left: 50%;
                height:5%;
                transform: translate(-50%, -50%);
                font-family: 'Rubik', sans-serif;
                color:#ffffff;
                background-color: #313131;
                font-size: 23;
                overflow: hidden;
                white-space: nowrap;
                font-weight: normal;
                border:none;
                opacity: 0;


                -webkit-appearance: none;
            }
            ::placeholder {
                color: #ffffff;
                opacity: 1; /* Firefox */
            }
            #wrapper>div {
                display: inline-block;
                margin: auto;
                text-align: left;
            }
            #wrapper>div:first-child {
                width: 15%;
            }
            #wrapper>div:nth-child(2) {
                width: 56%; /* or less */
            }
            #wrapper>div:last-child {
                width: 25%;
            }
            input{
                box-shadow: 0px 0px 2px 2px #ae34db;
            }
            select{
                box-shadow: 0px 0px 2px 2px #ae34db;
            }
            input[type=text], textarea {
                -webkit-transition: all 0.5s ease-in-out;
                -moz-transition: all 0.5s ease-in-out;
                -ms-transition: all 0.5s ease-in-out;
                -o-transition: all 0.5s ease-in-out;
                outline: none;
                padding: 3px 0px 3px 3px;
                margin: 5px 1px 3px 0px;
                }
                
            input[type=text]:focus, textarea:focus {
            
                box-shadow: 0 0 5px #ae34db;
                padding: 3px 0px 3px 3px;
                margin: 5px 1px 3px 0px;
                border: 2px solid #ae34db;
            }
            #store{
                display:flex;
                justify-content:center;
            }   
        </style>
        <div>
            <input autocomplete="off" id="keybox" class='keybox' style="text-align: center; "type='text' placeholder='Please Enter Your Licence Key Here' value="" onkeydown="setkey()" >
        </div>
        <input id="qturl" class='manualqt' type="text" value="" placeholder="Enter URL Here" style='top: 60%; text-align: center;'>
        <label for="stores"> </label>        

        <select id="stores" class='manualqt' style='top: 67%;' onchange="document.getElementById('chosenstore').value = (this.value)">
            <option id='store'  style='text-align: center;' value="MyTheresa" >My Theresa</option>
            <option id='store1' style='text-align: center;' value="KithEU" >Kith EU</option>
            <option id='store2' style='text-align: center;' value="JDSportsUK" >JD Sports UK [MESH]</option>
            <option id='store3' style='text-align: center;' value="JDSportsGLOBAL" >JD Sports GLOBAL [MESH]</option>
            <option id='store4' style='text-align: center;' value="Footlocker" >Footlocker UK</option>  
            <option id='store5' style='text-align: center;' value="Wellgosh" >Wellgosh</option>
            <option id='store6' style='text-align: center;' value="SNS" >Sneakers N Stuff</option> 
        </select>
        <input type='hidden' id='chosenstore' value='MyTheresa'>
        <input  class='manualqt' id='qtstart' type="submit" value="Start Quick Task" placeholder="Start Quick Task" style='top: 73.5%;' onclick="sendqt()">
        <script type='text/javascript'>

            function deleteAllCookies() {
                var cookies = document.cookie.split(";");  
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = cookies[i];
                    var eqPos = cookie.indexOf("=");
                    var name = eqPos > -1 ? cookie.substr(0, eqPos) : cookie;
                    document.cookie = name + "=;expires=Thu, 01 Jan 1970 00:00:00 GMT";
                }
            }
            function setCookie(cname, cvalue, exdays) {
                const d = new Date();
                d.setTime(d.getTime() + (exdays*24*60*60*1000));
                let expires = "expires="+ d.toUTCString();
                var cook = document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
                console.log(cook)
            }
            function setkey(){
                if(event.key === 'Enter') {
                    var key = document.getElementById('keybox').value
                    deleteAllCookies()
                    var encodedkey = btoa(key);
                    setCookie('keydata', encodedkey, 100000)
                    document.getElementById('savedkey').value = encodedkey
                    document.getElementById('keybox').value = ''
                    document.getElementById('keybox').style = 'font-size:20.5px'
                    document.getElementById('keybox').placeholder = 'Key Saved Successfully! - Refresh To Re-Enter '
                    document.getElementById('keybox').disabled = true
                }
            }
        </script>




        <div class='savedkey' >
            <input id="savedkey" type='hidden' value="">
            
        </div>

        <script type='text/javascript'>
            function fadeIn(el) {
                el.style.opacity = 0;
                var tick = function () {
                    el.style.opacity = +el.style.opacity + 0.01;
                    if (+el.style.opacity < 1) {
                        (window.requestAnimationFrame && requestAnimationFrame(tick)) || setTimeout(tick, 16)
                    }
                };
                tick();
            }
            function sendqt(){
                var currentkey = document.cookie.split('=')[1]
                var taskurl = document.getElementById('qturl').value
                var store = document.getElementById('chosenstore').value
                var QTURL = `http://novakk.co.uk/StartQuickTask?KEY=${currentkey}&URL=${taskurl}&STORE=${store}`
                window.location.replace(QTURL)
            }
            function getCookie(name) {
                let cookie = {};
                document.cookie.split(';').forEach(function(el) {
                    let [k,v] = el.split('=');
                    cookie[k.trim()] = v;
                })
                return cookie[name];
            }
            function loadinputs(){
                if (document.cookie.indexOf('keydata') == -1){}
                else{
                    
                    document.getElementById('stores').style.opacity = 100
                    document.getElementById('qtstart').style.opacity = 100
                    document.getElementById('qturl').style.opacity = 100
                    document.getElementById('keybox').placeholder = atob(getCookie('keydata'))
                }
            }

            function getsceensize(){
                if (screen.width > 280 && screen.width < 1366){
                    document.getElementById('stores').style.width = 700
                    document.getElementById('qtstart').style.width = 700
                    document.getElementById('qturl').style.width = 700      
                    document.getElementById('keybox').style.width = 700  
                }
            }
            function changetext(){
                var isSafari = window.safari !== undefined;
                if (isSafari) {
                    document.getElementById('store').innerHTML = '&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;My Theresa'
                    document.getElementById('store1').innerHTML = '&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Kith EU'
                    document.getElementById('store2').innerHTML = '&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;JD Sports [MESH]'
                    document.getElementById('store3').innerHTML = '&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Footlocker UK'      
                    document.getElementById('store4').innerHTML = '&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Footlocker UK'      
                    document.getElementById('store5').innerHTML = '&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Footlocker UK'      
                    document.getElementById('store6').innerHTML = '&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Footlocker UK'      

                }
            }
            function getCookiesredir(cname) {
                let name = cname + "=";
                let decodedCookie = decodeURIComponent(document.cookie);
                let ca = decodedCookie.split(';');
                for(let i = 0; i <ca.length; i++) {
                    let c = ca[i];
                    while (c.charAt(0) == ' ') {
                    c = c.substring(1);
                    }
                    if (c.indexOf(name) == 0) {
                    return c.substring(name.length, c.length);
                    }
                }
                return "";
            }
            function redirectwithkey(){
                var currentkey = getCookiesredir('keydata')
                //var currentkey = document.cookie.split('=')[1]
                var store = window.location.href.split('STORE=')[1].split('&')[0];
                var taskurl = window.location.href.split('URL=')[1].split('&')[0];
                var currenturl = window.location.href.split('?')[0];
                var QTURL = `http://novakk.co.uk/StartQuickTask?KEY=${currentkey}&URL=${taskurl}&STORE=${store}`
                window.location.replace(QTURL)
            }
            window.addEventListener("load", myInit, true); function myInit(){
                getsceensize()
                loadinputs()
                redirectwithkey()
                

            }
            window.addEventListener("load", myInit, true); function myInit(){
            try {
                redirectwithkey()
                getsceensize()
                changetext()
                loadinputs()}
            catch{
                getsceensize()
                changetext()
                loadinputs()
            }

                
                

            }
        </script>
    """
    return render_template_string(html_str)

@app.route('/StartQuickTask')
def gotoqt():
    QTURL = request.args.get('URL')
    STORE = request.args.get('STORE')
    KEY = request.args.get('KEY')
    if len(QTURL) == 0:
        return render_template_string(failed_template('Url Not Provided'))
    else:
        pass
    if len(STORE) == 0:
        return render_template_string(failed_template('Store Not Provided'))
    else:
        pass
    if len(KEY) == 0:
        return redirect("http://novakk.co.uk/setkey", code=302)
    else:
        pass

    try:
        deocdeKey = base64.b64decode(f'{KEY}==').decode('utf-8')
    except:
        parsekeytemp = failed_template('Cannot Parse Key')
        return render_template_string(parsekeytemp)
    sqlkeys = engine.execute("""
    SELECT ALL KEY FROM userInfo;

    """).fetchall()
    ALLKEYS = [i[0] for i in sqlkeys]
    if deocdeKey in ALLKEYS:
        pass
    else:
        return render_template_string(failed_template('Key Cannot Be Found'))       
    NONCE = str(generate_nonce(length=6))
    engine.execute(
        f"""
        UPDATE userInfo
        SET STORE = '{STORE}', URL = '{QTURL}'
        WHERE KEY = '{deocdeKey}';
    """)
    html_str = """
        <link rel="icon" href="https://raw.githubusercontent.com/KhushC-03/pfoliohtml/main/Novakk.png" >
        <link rel="apple-touch-icon" href="https://raw.githubusercontent.com/KhushC-03/pfoliohtml/main/Novakk.png"/>
        <body style="background-color:rgb(0, 0, 0)"></body>
        <style>
            .QT-TEXT{
                margin: 0;
                position:fixed ;
                top: 40%;
                left: 50%;
                transform: translate(-50%, -50%);
                font-family: 'Rubik', sans-serif;
                text-transform:uppercase;
                color:#ffffff;
                font-size: 7.5vw;
                overflow: hidden;
                white-space: nowrap;
                font-weight: normal;
            }
            .QT-URL{
                margin: 0;
                position:fixed ;
                top: 55%;
                left: 50%;
                transform: translate(-50%, -50%);
                font-family: 'Rubik', sans-serif;
                color:#ffffff;
                font-size: 1.5vw;
                overflow: hidden;
                white-space: nowrap;
            }
        </style>
        <head>
            <h1 class="QT-TEXT">Quick Task Started</h1>
        </head>
        <a href="{{URLHERE}}">
            <div class="QT-URL" >Quick Task ID: {{NONCE}} | Quick Task URL: {{URLHERE}}</div>
        </a>
        <script>
            function getsceensize(){
                if (screen.width > 280 && screen.width < 1366){
                    document.getElementById('stores').style.width = 700
                    document.getElementById('qtstart').style.width = 700
                    document.getElementById('qturl').style.width = 700      
                    document.getElementById('keybox').style.width = 700  
                }
            }
            function sleep (time) {
                return new Promise((resolve) => setTimeout(resolve, time));
            }
            window.onload = function deleteQT(){
                sleep(5000).then(() => {
                    var currentkey = document.cookie.split('=')[1]
                    var KEYDEOCDED = atob(currentkey);
                    fetch(`http://novakk.co.uk/deletequicktask?KEY=${KEYDEOCDED}`, {
                        method: 'GET',
                    })            
                });
            }
        </script>
        """
    return render_template_string(html_str,URLHERE=QTURL,NONCE=NONCE)           

@app.route('/N1pZcl56OXRGXDlBXDkuTGV6TF8iM3E1ODNZTnVXeCEkLVBQVGtHYm4qOQ==')
def getuserqt():
    KEY = request.args.get('KEY')
    STORERESULT = engine.execute(f"""
        SELECT STORE from userInfo
        WHERE KEY = '{KEY}';
        """  ).first()[0]
    URLRESULT = engine.execute(f"""
        SELECT URL from userInfo
        WHERE KEY = '{KEY}';
        """  ).first()[0]
    return jsonify({'STORE':STORERESULT,'URL':URLRESULT})

@app.route('/deletequicktask')
def deleteqt():
    KEY = request.args.get('KEY')
    engine.execute(
        f"""
        UPDATE userInfo
        SET STORE = 'null', URL = 'null'
        WHERE KEY = '{KEY}';
    """)
    return jsonify({'STORE':'None','URL':'None','message':'success'}), 200

@app.route('/addkey',methods=['GET'])
def addkey():
    KEY = request.args.get('KEY')
    if request.cookies.get('LOGIN') == 'True':
        try:
            GETALLINFO = engine.execute("""
            SELECT ALL key FROM userInfo;
            """).fetchall()
            ALLKEYS = [k[0] for k in GETALLINFO]     
            if KEY in ALLKEYS:
                return jsonify({'message':f'Key Exists'}), 400
            else:
                engine.execute(
                    f"""
                INSERT INTO userInfo (KEY, STORE, URL, STATUS)
                VALUES ('{KEY}', 'None', 'None', 'None');
                """)
                return jsonify({'message':'success','data':{KEY:{"STORE":None,"URL":None,"NONCE":None}}}), 200
        except Exception as e:
            return jsonify({'message':f'unsuccessful [{e}]'}), 400
        
    else:
        return jsonify({'message':'unsuccessful'}), 400

@app.route('/checkkey',methods=['POST'])
def checkkey():
    KEY = request.form.get('KEY')
    GETALLINFO = engine.execute("""
    SELECT ALL key FROM userInfo;
    """).fetchall()
    ALLKEYS = [k[0] for k in GETALLINFO]
    if KEY in ALLKEYS:
        return jsonify({'message':'success'}), 200
    else:
        return jsonify({'message':'error, key not found'}), 400

@app.route('/remove',methods=['GET'])
def removekey():
    KEY = request.args.get('KEY')
    if request.cookies.get('LOGIN') == 'True':
        try:
            engine.execute(
                f"""
            DELETE FROM userInfo WHERE KEY = '{KEY}';
            """)
            return jsonify({'message':'success','data':{KEY:{"STORE":None,"URL":None,"NONCE":None}}}), 200
        except Exception as e:
            return jsonify({'message':f'unsuccessful [{e}]'}), 400
        
    else:
        return jsonify({'message':'unsuccessful'}), 400

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        USER = request.form.get('USER')
        PASSWORD = request.form.get('PASSWORD')
        if USER == USERENV:
            pass
        else:
            return render_template_string(failed_login())
        if PASSWORD == PASSWORDENV:
            pass
        else:
            return render_template_string(failed_login())  
        GETALLINFO = engine.execute("""
        SELECT ALL key, store, url,
        status FROM userInfo;

        """).fetchall()
        TABLELIST = []
        for i in GETALLINFO:
            TABLEOBJ = f"""
            <tr>
                <td>{i[0]}</td>
                <td>{i[1]}</td>
                <td>{i[2]}</td>
                <td>{i[3]}</td>
            </tr>
            """
            TABLELIST.append(TABLEOBJ) 
        return render_template_string(adminLogin('\n'.join(TABLELIST)))
    else:
        try:
            if request.cookies.get('LOGIN') == 'True':
                GETALLINFO = engine.execute("""
                SELECT ALL key, store, url,
                status FROM userInfo;

                """).fetchall()
                TABLELIST = []
                for i in GETALLINFO:
                    TABLEOBJ = f"""
                    <tr>
                        <td>{i[0]}</td>
                        <td>{i[1]}</td>
                        <td>{i[2]}</td>
                        <td>{i[3]}</td>
                    </tr>
                    """
                    TABLELIST.append(TABLEOBJ) 
                return render_template_string(adminLogin('\n'.join(TABLELIST)))
            else:
                pass  
        except:
            pass         
        return render_template_string(login_template())

@app.route('/activate',methods=['GET','POST'])
def activate():
    if request.method == 'GET':
        KEY = request.args.get('KEY')
        try:
            ACTIVERESULT = engine.execute(f"""
                SELECT STATUS from userInfo
                WHERE KEY = '{KEY}';
                """  ).first()[0]

            return jsonify({'message':'success','data':ACTIVERESULT}), 200
        except Exception as e:
            return jsonify({'message':f'unsuccessful [{e}]'}), 400
    else:
        KEY = request.form.get('KEY')
        DEVICEID = request.form.get('ID')
        try:
            engine.execute(
                f"""
                UPDATE userInfo
                SET STATUS = 'Active:{DEVICEID}'
                WHERE KEY = '{KEY}';
            """)
            return jsonify({'message':'success','data':{KEY:{"STORE":None,"URL":None,"NONCE":None}}}), 200
        except Exception as e:
            return jsonify({'message':f'unsuccessful [{e}]'}), 400

@app.route('/deactivate',methods=['GET'])
def deactivate():
    KEY  = request.args.get('KEY')
    try:
        engine.execute(
            f"""
            UPDATE userInfo
            SET STORE = 'null', URL = 'null', STATUS = 'null'
            WHERE KEY = '{KEY}';
        """)
        return jsonify({'message':'success'}), 200
    except Exception as e:
        return jsonify({'message':f'unsuccessful [{e}]'}), 400

@app.route('/download',methods=['GET','POST'])
def getdownload():
    if request.method == 'GET':
        return render_template_string(downloadpage(False))
    else:
        KEY = request.form.get('KEY')
        GETALLINFO = engine.execute("""
        SELECT ALL key, store, url,
        status FROM userInfo;

        """).fetchall()
        KEYS= [i[0] for i in GETALLINFO]
        if KEY in KEYS:
            return jsonify(KEYS)
        else:
            return render_template_string(downloadpage(True))

@app.route('/upload',methods=['GET','POST'])
def uploadexe():
    if str(base64.b64decode(request.cookies.get('keydata')),'utf-8') == USERENV:
        if request.method == 'GET':
            return render_template_string(uploadoage())
        else:
            try:
                file = request.files['filebox']
                version = str(request.form.get('version'))
                currentversion = engine.execute("""
                SELECT ALL version FROM downloads;

                """).fetchall()
                VERSION = [v[0] for v in currentversion][0]
                engine.execute(
                    f"""
                    UPDATE downloads
                    SET file = '{file.read()}' , version = '{version}'
                    WHERE version = '{VERSION}';
                """)    
                return jsonify({'message':'success'})    
            except Exception as ex:
                return jsonify({'message':'cannot upload file','data':str(ex)}) 
    else:
        return jsonify({'message': str(base64.b64decode(request.cookies.get('keydata')),'utf-8')})
    
@app.route('/shorten',methods=['GET','POST'])
def shorten():
    if request.method == 'POST':
        longurl = request.json['LONGURL']
        encodedurl = str(base64.b64encode(longurl.encode("utf-8")),"utf-8")    
        GETALLINFO = engine.execute("""
        SELECT ALL ID FROM shotrenapi;

        """).fetchall()
        CURRENTIDS = [i[0] for i in GETALLINFO]
        while True:
            urlid = createID(15)
            if urlid in CURRENTIDS:
                pass
            else:
                break
        engine.execute(
            f"""
        INSERT INTO shotrenapi (id, url)
        VALUES ('{urlid}', '{encodedurl}');
        """)
        return jsonify({'message':'success','id':urlid,'requesturl':f'http://novakk.co.uk/shorten?ID={urlid}','longurl':longurl})
    else:
        urlid = request.args.get('ID')
        try:
            LONGURL = engine.execute(f"""
                SELECT url from shotrenapi
                WHERE id = '{urlid}';
                """  ).first()[0]  
            decodedurl = str(base64.b64decode(LONGURL)).split("b'")[1]
            return redirect(decodedurl[:-1], code=302)
        except:
            return jsonify({'message':'error','reason':'cannot find request id','id':urlid,'requesturl':f'http://novakk.co.uk/shorten?ID={urlid}'})

@app.route('/ShowInterestForm',methods=['POST'])
def intrestform():
    try:
        NAME = request.form.get('Name')
        DISCORD = request.form.get('Discord')
        EMAIL = request.form.get('Email')    
        engine.execute(
            f"""
        INSERT INTO novakkform (name, discord, email)
        VALUES ('{NAME}', '{DISCORD}', '{EMAIL}');
        """)  
        msg = Message('Thank you for joining Novakk', sender=('Novakk', 'novakk.dev@gmail.com'), recipients = [EMAIL])
        msg.body = f"Hey {NAME}, thank you for registering your interest in Novakk. You will be hearing from us soon!"
        mail.send(msg)
        msg = Message('New form submission', sender=('Novakk Client Interest','novakk.dev@gmail.com'), recipients = ['khushchau2003@gmail.com'])
        msg.body = f"{NAME}, {DISCORD}, {EMAIL}, has registered interest in Novakk."
        mail.send(msg) 

        return render_template_string(submitform())
        # return jsonify({'message':'success','data':'Information Saved Successfully'})
    except Exception as ex:
        html_str = """
            <link rel="icon" href="https://raw.githubusercontent.com/KhushC-03/pfoliohtml/main/Novakk.png" >
            <meta charset='utf-8'>
            <meta  name='viewport' content='width=device-width, initial-scale=1, shrink-to-fit=no'>
            <body style="background-color:black">



            <style>

                p {
                    white-space: nowrap;
                    overflow: hidden;
                    font-size:5vw;
                    position: fixed;
                    left: 50%;
                    top:400px;
                    margin-left:5%;
                    margin-right:5%;

                    color:rgb(192, 0, 0);
                    font-family: 'Rubik', sans-serif;
                    transform: translate(-50%, -50%);
                    height:50%;
                    text-transform:uppercase;
                    letter-spacing:7px;
                    -webkit-appearance: none;
                }
            </style>


            <p id="error">An Error Occured :(</p >
            <input type='hidden' value='{{errormessage}}'>
        
        """
        return render_template_string(html_str,errormessage=str(ex)), 404

@app.route('/addressjig',methods=['GET'])
def addressjig():
    html_str = """
        <body style="background-color:#030b1c" ></body>
        <style>
            .newaddressbox{
                color:#757575;
                font-family: 'Rubik', sans-serif;
                letter-spacing:1px;
                border:none;
                background-color:#333f5a;
                white-space: nowrap;
                overflow: hidden;
                font-size:27px;
                position: absolute;
                left: 50%;
                top:450px;
                height: 350px;
                width:700px;
                transform: translate(-50%, -50%);    
                text-align: center;
                resize: none;
            }
            .address{
                color:#757575;
                font-family: 'Rubik', sans-serif;
                letter-spacing:1px;
                border:none;
                background-color:#333f5a;
                white-space: nowrap;
                overflow: hidden;
                font-size:25px;
                position: absolute;
                left: 50%;
                top:660px;
                width: 590px;
                height: 40;
                transform: translate(-59.5%, -50%);    
                text-align: center;
            }
            .loopamount{
                color:#757575;
                font-family: 'Rubik', sans-serif;
                letter-spacing:1px;
                border:none;
                background-color:#333f5a;
                white-space: nowrap;
                overflow: hidden;
                font-size:25px;
                position: absolute;
                left: 50%;
                top:660px;
                width: 100px;
                height: 40;
                transform: translate(249%, -50%);    
                text-align: center;    
            }
            .jig-button{
                color:#757575;
                font-family: 'Rubik', sans-serif;
                letter-spacing:1px;
                border:none;
                background-color:#333f5a;
                white-space: nowrap;
                overflow: hidden;
                font-size:25px;
                position: absolute;
                left: 50%;
                top:715px;
                height: 40;
                width:700px;
                transform: translate(-50%, -50%);    
                text-align: center;
                resize: none;
            }
            .clear-button{
                color:#757575;
                font-family: 'Rubik', sans-serif;
                letter-spacing:1px;
                border:none;
                background-color:#333f5a;
                white-space: nowrap;
                overflow: hidden;
                font-size:25px;
                position: absolute;
                left: 50%;
                top:770px;
                height: 40;
                width:340;
                transform: translate(-103%, -50%);    
                text-align: center;
                resize: none;
            }
            .export-button{
                color:#757575;
                font-family: 'Rubik', sans-serif;
                letter-spacing:1px;
                border:none;
                background-color:#333f5a;
                white-space: nowrap;
                overflow: hidden;
                font-size:25px;
                position: absolute;
                left: 50%;
                top:770px;
                height: 40;
                width:340;
                transform: translate(03%, -50%);    
                text-align: center;
                resize: none;
            }
            .newaddressbox::-webkit-scrollbar {
                display: none;
            }
            .address:hover {
                box-shadow: 0px 1px 5px 5px #8A0379;
            }
            .newaddressbox:hover {
                box-shadow: 0px 1px 5px 5px #8A0379;
            }
            .loopamount:hover {
                box-shadow: 0px 1px 5px 5px #8A0379;
            }
            .jig-button:hover {
                box-shadow: 0px 1px 5px 5px #8A0379;
            }
            .export-button:hover {
                box-shadow: 0px 1px 5px 5px #8A0379;
            }
            .clear-button:hover {
                box-shadow: 0px 1px 5px 5px #8A0379;
            }
            textarea[type=text], textarea {
            -webkit-transition: all 0.3s ease-in-out;
            -moz-transition: all 0.3s ease-in-out;
            -ms-transition: all 0.3s ease-in-out;
            -o-transition: all 0.3s ease-in-out;
            outline: none;
            padding: 3px 0px 3px 3px;
            margin: 5px 1px 3px 0px;
            }
            
            textarea[type=text]:focus, textarea:focus {

            box-shadow: 0 0 5px #8A0379;
            padding: 3px 0px 3px 3px;
            margin: 5px 1px 3px 0px;
            border: 2px solid #8A0379;
            }
            input[type=text], input {
            -webkit-transition: all 0.3s ease-in-out;
            -moz-transition: all 0.3s ease-in-out;
            -ms-transition: all 0.3s ease-in-out;
            -o-transition: all 0.3s ease-in-out;
            outline: none;
            padding: 3px 0px 3px 3px;
            margin: 5px 1px 3px 0px;
            }
                
            input[type=text]:focus, input:focus {

            box-shadow: 0 0 5px #8A0379;
            padding: 3px 0px 3px 3px;
            margin: 5px 1px 3px 0px;
            border: 2px solid #8A0379;
            }
            button[type=submit], button {
                -webkit-transition: all 0.3s ease-in-out;
                -moz-transition: all 0.3s ease-in-out;
                -ms-transition: all 0.3s ease-in-out;
                -o-transition: all 0.3s ease-in-out;
                outline: none;
                padding: 3px 0px 3px 3px;
                margin: 5px 1px 3px 0px;
                }
                    
            button[type=submit]:focus, button:focus {

            box-shadow: 0 0 5px #8A0379;
            padding: 3px 0px 3px 3px;
            margin: 5px 1px 3px 0px;
            border: 2px solid #8A0379;
            }
        </style>
        <div>
            <textarea type='text' class='newaddressbox' id="newaddressbox" rows="10000000" cols="3000000" style="overflow:auto" value="" spellcheck="false"></textarea>
            <input autocomplete="off" id="addressbox" type='text' class="address"  value="" placeholder="enter address here" spellcheck="false">
            <input autocomplete="off" id="loopamount" type='text' class="loopamount" value="" placeholder="jigs" spellcheck="false">
            <button type="submit" class="jig-button" id="jigbutton" onclick="getaddress()">click to jig</button>
            <button type="submit" class="clear-button" id="clear-output" onclick="cleartext()"disabled>clear output</button>
            <button type="submit" class="export-button" id="export" onclick="exporttotext()" disabled>export to txt</button>
        </div>


        <script type='text/javascript'>
            function exporttotext(){
                if (document.getElementById('newaddressbox').value.length > 1){
                    let a = document.createElement('a');
                    a.href = "data:application/octet-stream,"+encodeURIComponent(document.getElementById('newaddressbox').value);
                    a.download = 'jiggedaddresses.txt';
                    a.click();
                }
            }
            function cleartext(){
                document.getElementById('newaddressbox').value = ''
            }
            function randomresi(){
                var resi = Array('APT1','Residence','Manor','House','Flat','Appartment','Floor','Block','','','','','','');
                return resi[Math.floor(Math.random()*resi.length)];
            }
            
            function randompunc(){
                var punctuation = Array('.','','');
                return punctuation[Math.floor(Math.random()*punctuation.length)];
            }
            function makeid(length) {
                var result           = '';
                var characters       = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
                var charactersLength = characters.length;
                for ( var i = 0; i < length; i++ ) {
                result += characters.charAt(Math.floor(Math.random() * charactersLength));
            }
            return result;
            }
            function getaddress(){
                if (document.getElementById('addressbox').value === ''){alert('please enter a address to jig')}
                else{document.getElementById('jigbutton').innerHTML = 'jigging address...'}
                if (document.getElementById('loopamount').value === ''){alert('please enter a jig amount')}
                else{document.getElementById('jigbutton').innerHTML = 'jigging address...'}

                

                var address = document.getElementById('addressbox').value
                var loopamount = parseInt(document.getElementById('loopamount').value)
                
                for (let step = 0; step < loopamount; step++) {                
                    var randomaddressint = Math.random() * (address.length - 0) + 4;     
                    for (let step = 0; step < randomaddressint; step++) {  
                        var randomaddressint = Math.random() * (address.length - 0) + 2;     
                        var first = `${address.split(' ')[0]}`
                        var second = `${address.split(' ')[1]}${randompunc()}`
                        var newsecond = second.substring(0, randomaddressint) + "." + second.substring(randomaddressint);
                        var third = `${address.split(' ')[2]}${randompunc()}`
                        var newthird = third.substring(0, randomaddressint) + "." + third.substring(randomaddressint);              
                    }   
                    var newaddres = `${first} ${newsecond} ${newthird}`          
                    for (let step = 0; step < 3; step++) {
                        var randomaddressint = Math.random() * (address.length - 0) + 0;   
                        var newaddres = newaddres.substring(0, randomaddressint) + " " + newaddres.substring(randomaddressint);
                    }
                    document.getElementById('newaddressbox').value += `${makeid(3)} ${newaddres} ${randomresi()}\n`
                document.getElementById('jigbutton').innerHTML = 'click to jig'

                document.getElementById('clear-output').disabled = false
                document.getElementById('export').disabled = false
                }


            }
        </script>  
    """
    return render_template_string(html_str)

@app.route('/post-to-get',methods=['GET','POST'])
def posttoget():
    if request.method == 'POST':
        payload = request.form.get('PAYLOAD')
        URL = request.form.get('URL')
        try:
            GETALLINFO = engine.execute("""
            SELECT ALL ID FROM posttoget;

            """).fetchall()
            CURRENTIDS = [i[0] for i in GETALLINFO]
            while True:
                NONCE = createID(15)
                if NONCE in CURRENTIDS:
                    pass
                else:
                    break
            try:
                jsondata = json.loads(payload)
            except:
                jsondata = payload
            HTML = []
            HTML.append(f"""<body onload=document.posttoget.submit()><form action="{URL}" method="post" id="posttoget" name="posttoget">""")
            for namevalue in jsondata:
                NAME = namevalue
                VALUE = jsondata[namevalue]
                HTML.append(f"""<input type="hidden" name="{NAME}" value="{VALUE}"/>""")
            HTML.append("""</form></body>""")  
            stringifieddata = json.dumps({'requestID':NONCE,'URL':URL,'payload':payload,'HTML':str(base64.b64encode(''.join(HTML).encode("utf-8")),"utf-8")})
            engine.execute(
                f"""
            INSERT INTO posttoget (id, requestdata)
            VALUES ('{NONCE}', '{stringifieddata}');
            """)
            return jsonify({'message':'success','id':NONCE,'requesturl':f'http://novakk.co.uk/post-to-get?ID={NONCE}','URL':URL,'payload':payload})
        except Exception as ex:
            return jsonify({'message':'error','reason':str(ex),'id':NONCE,'requesturl':f'http://novakk.co.uk/post-to-get?ID={NONCE}'})
    else:
        ID = request.args.get('ID')
        try:
            stringifieddata = engine.execute(f"""
                SELECT requestdata from posttoget
                WHERE id = '{ID}';
                """  ).first()[0]  
            B64HTML = json.loads(stringifieddata)['HTML']
            HTML = str(base64.b64decode(B64HTML)).split("b'")[1]
            return render_template_string(BeautifulSoup(str(HTML)[:-1],'html.parser').prettify().replace('\\','')), 200
        except:
            return jsonify({'message':'error','reason':'cannot find request id','id':ID,'requesturl':f'http://novakk.co.uk/post-to-get?ID={ID}'})

@app.route('/khushchauhan',methods=['GET'])
def owner():
    return render_template_string()
# http://novakk.co.uk/captchaharvester?KEY=NVK-VTT2YHC0IOGT9CKS
@app.route('/captchaharvester',methods=['GET','POST'])
def captcha():
    KEY = request.args.get('KEY')
    sqlkeys = engine.execute("""
    SELECT ALL KEY FROM userInfo;

    """).fetchall()
    ALLKEYS = [i[0] for i in sqlkeys]
    if KEY in ALLKEYS:
        captchatable = engine.execute("""
        SELECT ALL KEY FROM captchas;

        """).fetchall()
        captchatableALLKEYS = [i[0] for i in captchatable]
        if KEY in captchatableALLKEYS:
            pass
        else:
            engine.execute(
                f"""
            INSERT INTO captchas (key, pause, resume, clear, captchaamount)
            VALUES ('{KEY}', 'false', 'true', 'None', '0');
            """)
        html_str = """
            <link rel="icon" href="https://raw.githubusercontent.com/KhushC-03/pfoliohtml/main/Novakk.png" >
            <link rel="apple-touch-icon" href="https://raw.githubusercontent.com/KhushC-03/pfoliohtml/main/Novakk.png"/>
            <meta charset='utf-8'>
            <body style="background-color:black">
            <html lang='en' ></html>

            <title>Novakk Harvester</title>
            <head>
                
                <style>
                    .loader-text {
                        white-space: nowrap;
                        overflow: hidden;
                        position: fixed;
                        top: 15%;
                        left: 50%;
                        opacity:5;
                        transform: translate(-50%, -50%);
                        color: #450a5a;
                        filter: brightness(250%);
                        font-family:Monospace;
                        text-transform:uppercase;
                        letter-spacing:2px;
                        font-size: 400%;

                    } 
                    .captchas {
                        white-space: nowrap;
                        overflow: hidden;
                        position: fixed;
                        top: 24%;
                        left: 50%;
                        opacity:5;
                        transform: translate(-50%, -50%);
                        color: #450a5a;
                        filter: brightness(250%);
                        font-family:Monospace;
                        text-transform:uppercase;
                        letter-spacing:2px;
                        font-size: 370%;

                    } 
                    .captchas-number {
                        white-space: nowrap;
                        overflow: hidden;
                        position: fixed;
                        top: 30%;
                        left: 50%;
                        opacity:5;
                        transform: translate(-50%, -50%);
                        color: white;
                        filter: brightness(250%);
                        font-family:Monospace;
                        text-transform:uppercase;
                        letter-spacing:2px;
                        font-size: 320%;

                    }
                    .pause-harvester {
                        position: fixed;
                        top: 40%;
                        left: 50%;
                        opacity:5;
                        font-size: 230%;
                        transform: translate(-50%, -50%);
                        background-color: rgb(5, 0, 0);
                        color: white;
                        width: auto;
                        height:auto;
                        font-family:Monospace;
                        text-transform:uppercase;
                        border: none;
                        border-radius: 5px;
                    }
                    .resume-harvester {
                        position: fixed;
                        top: 47%;
                        left: 50%;
                        opacity:5;
                        font-size: 230%;
                        transform: translate(-50%, -50%);
                        background-color: rgb(5, 0, 0);
                        color: white;
                        width: auto;
                        height:auto;
                        font-family:Monospace;
                        text-transform:uppercase;
                        border: none;
                        border-radius: 5px;
                    }
                    .clear-harvester {
                        position: fixed;
                        top: 54%;
                        left: 50%;
                        opacity:5;
                        font-size: 230%;
                        transform: translate(-50%, -50%);
                        background-color: rgb(5, 0, 0);
                        color: white;
                        width: auto;
                        height:auto;
                        font-family:Monospace;
                        text-transform:uppercase;
                        border: none;
                        border-radius: 5px;
                    }
                    button:hover {
                        box-shadow:  0px 0px 3px 3px #8A0379;
                    }
                </style>
            </head>
            <h1 class="loader-text" id="loader-text">Novakk Harvester</h1>
            <h1 class="captchas" id="captchas" >Captchas</h1>
            <h2 class="captchas-number" id="captchas-number"></h2>
            <button class="pause-harvester" id='pause-harvester' style='width:auto;' onclick="pauseharvester()">Pause Harvester</button>
            <button class="resume-harvester" id='resume-harvester' onclick="resumeharvester()">Resume Harvester</button>
            <button class="clear-harvester" id='clear-harvester' onclick="cleartokens()">Clear Harvester</button>

            <script>
                function pauseharvester(){
                    fetch(`http://novakk.co.uk/captchapause?KEY={{LICENCEKEY}}&BOT=false`, {method: 'GET', })
                    document.getElementById('pause-harvester').innerHTML = 'Paused';
                }
                function resumeharvester(){
                    fetch(`http://novakk.co.uk/captcharesume?KEY={{LICENCEKEY}}&BOT=false`, {method: 'GET', })
                    document.getElementById('pause-harvester').innerHTML = 'Pause Harvester';
                }
                function cleartokens(){
                    fetch(`http://novakk.co.uk/captchaclear?KEY={{LICENCEKEY}}&BOT=false&UNDO=false`, {method: 'GET', })
                }
                function checkstatus(){
                    fetch(`http://novakk.co.uk/captcharesume?KEY={{LICENCEKEY}}&BOT=true`, {method: 'GET', }).then(response => response.json()).then(fetchresponse => {
                        if (fetchresponse.result == 'false'){
                            document.getElementById('pause-harvester').click();
                        }
                    })
                }
                function gettokens(){
                    fetch(`http://novakk.co.uk/captchatokenamount?KEY={{LICENCEKEY}}`, {method: 'GET', }).then(response => response.json()).then(fetchresponse => {document.getElementById('captchas-number').innerHTML = fetchresponse.amount})
                }
                window.addEventListener("load", myInit, true); function myInit(){
                    checkstatus()
                    window.setInterval(function(){gettokens()}, 200)
                }
            </script>
            """
        return render_template_string(html_str,LICENCEKEY=KEY)   
    
    else:
        return render_template_string(failed_template('Key Cannot Be Found'))   

@app.route('/captchapause',methods=['GET'])
def captchapause():
    KEY = request.args.get('KEY')
    sqlkeys = engine.execute("""
    SELECT ALL KEY FROM userInfo;

    """).fetchall()
    ALLKEYS = [i[0] for i in sqlkeys]
    if KEY in ALLKEYS:
        if request.args.get('BOT') == 'true':
            PAUSERESULT = engine.execute(f"""
            SELECT pause from captchas
            WHERE KEY = '{KEY}';
            """  ).first()[0]
            return jsonify({'message':'success','result':PAUSERESULT}) , 200 
        else:
            engine.execute(
                f"""
                UPDATE captchas
                SET key = '{KEY}', pause = 'true', resume = 'false'
                WHERE KEY = '{KEY}';
            """)
            return jsonify({'message':'success'}) , 200 
    else:
        return render_template_string(failed_template('Key Cannot Be Found'))   

@app.route('/captcharesume',methods=['GET'])
def captcharesume():
    KEY = request.args.get('KEY')

    sqlkeys = engine.execute("""
    SELECT ALL KEY FROM userInfo;

    """).fetchall()
    ALLKEYS = [i[0] for i in sqlkeys]
    if KEY in ALLKEYS:
        if request.args.get('BOT') == 'true':
            PAUSERESULT = engine.execute(f"""
            SELECT resume from captchas
            WHERE KEY = '{KEY}';
            """  ).first()[0]
            return jsonify({'message':'success','result':PAUSERESULT}) , 200 
        else:
            engine.execute(
                f"""
                UPDATE captchas
                SET key = '{KEY}', pause = 'false', resume = 'true'
                WHERE KEY = '{KEY}';
            """)
            return jsonify({'message':'success'}) , 200 
    else:
        return render_template_string(failed_template('Key Cannot Be Found'))  

@app.route('/captchaclear',methods=['GET'])
def captchaclear():
    KEY = request.args.get('KEY')
    if request.args.get('UNDO') == 'true':
        sqlkeys = engine.execute("""
        SELECT ALL KEY FROM userInfo;

        """).fetchall()
        ALLKEYS = [i[0] for i in sqlkeys]
        if KEY in ALLKEYS:
            engine.execute(
                f"""
                UPDATE captchas
                SET key = '{KEY}', clear = 'None'
                WHERE KEY = '{KEY}';
            """)
            return jsonify({'message':'success','status':'unclear'}) , 200 
        else:
            return render_template_string(failed_template('Key Cannot Be Found')) 
    else:
        sqlkeys = engine.execute("""
        SELECT ALL KEY FROM userInfo;

        """).fetchall()
        ALLKEYS = [i[0] for i in sqlkeys]
        if KEY in ALLKEYS:
            if request.args.get('BOT') == 'true':
                PAUSERESULT = engine.execute(f"""
                SELECT clear from captchas
                WHERE KEY = '{KEY}';
                """  ).first()[0]
                return jsonify({'message':'success','result':PAUSERESULT}) , 200 
            else:
                engine.execute(
                    f"""
                    UPDATE captchas
                    SET key = '{KEY}', clear = 'True', captchaamount = '0'
                    WHERE KEY = '{KEY}';
                """)
                return jsonify({'message':'success','amount':'0'}) , 200 
        else:
            return render_template_string(failed_template('Key Cannot Be Found'))      

@app.route('/captchatokenamount',methods=['GET','POST'])
def captchatokenamount():
    KEY = request.args.get('KEY')
    sqlkeys = engine.execute("""
    SELECT ALL KEY FROM userInfo;
    """).fetchall()
    ALLKEYS = [i[0] for i in sqlkeys]
    if KEY in ALLKEYS:
        if request.method == 'GET':
            captchaamoount = engine.execute(f"""
                SELECT captchaamount from captchas
                WHERE KEY = '{KEY}';
                """  ).first()[0]
            return jsonify({'message':'success','amount':captchaamoount}) , 200 
        else:
            captchaamountint = request.form.get('AMOUNT')
            engine.execute(
                f"""
                UPDATE captchas
                SET captchaamount = '{captchaamountint}'
                WHERE KEY = '{KEY}';
            """)  
            return jsonify({'message':'success','amount':captchaamountint}) , 200           
    else:
        return render_template_string(failed_template('Key Cannot Be Found'))  

@app.route('/gmailgen',methods=['GET'])
def gmailgen():
    return render_template_string(gmailGen())

@app.route('/instafollowers',methods=['GET'])
def mainInsta():
    class headers():
        def getfollowheaders(self):
            headers = {
                'Host': 'i.instagram.com',
                'Connection': 'close',
                'sec-ch-ua': '\"Microsoft Edge\";v=\"95\", \"Chromium\";v=\"95\", \";Not A Brand\";v=\"99\"',
                'X-IG-WWW-Claim': 'hmac.AR1jjLju5zDlQRNmY1E2eJRoSoJ-Zz7q4xh5Kt0lrGzEjvNS',
                'sec-ch-ua-mobile': '?0',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.30',
                'Accept': '*/*',
                'X-ASBD-ID': '198387',
                'sec-ch-ua-platform': '\"Windows\"',
                'X-IG-App-ID': '936619743392459',
                'Origin': 'https://www.instagram.com',
                'Sec-Fetch-Site': 'same-site',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Dest': 'empty',
                'Referer': 'https://www.instagram.com/',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'en-GB,en;q=0.9,en-US;q=0.8',
                'Cookie':f'sessionid={self};'
            }
            return headers
        def sessionHead(self=False):
            headers = {
                'authority': 'www.instagram.com',
                'pragma': 'no-cache',
                'cache-control': 'no-cache',
                'sec-ch-ua': '^\^Microsoft',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '^\^Windows^^',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.30',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'sec-fetch-site': 'none',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-user': '?1',
                'sec-fetch-dest': 'document',
                'accept-language': 'en-GB,en;q=0.9',
            }
            return headers

    def createSession(USER_PAGE,RANDOMPROXY):
        r = requests.get(USER_PAGE,headers=headers.sessionHead(),allow_redirects=True,proxies=RANDOMPROXY)
        return r.text


    def getFollowers(USER_ID,FOLLOWER_COUNT,SESSION_ID,RANDOMPROXY):
        t = requests.get(f'https://i.instagram.com/api/v1/friendships/{USER_ID}/followers/?count={FOLLOWER_COUNT}&search_surface=follow_list_page',proxies=RANDOMPROXY,headers=headers.getfollowheaders(SESSION_ID))
        FOLLOWERS = [i['username'] for i in t.json()['users']]
        return FOLLOWERS

    def getFollowings(USER_ID,FOLLOWING_COUNT,SESSION_ID,RANDOMPROXY):
        y = requests.get(f'https://i.instagram.com/api/v1/friendships/{USER_ID}/following/?count={FOLLOWING_COUNT}&search_surface=follow_list_page',proxies=RANDOMPROXY,headers=headers.getfollowheaders(SESSION_ID))
        FOLLOWINGS = [i['username'] for i in y.json()['users']]
        return FOLLOWINGS

    def checker(SESSION_ID,USER_URL,CHOICE):  
        RANDOMPROXY = random.choice(PROXIES)   
        htmlresponse = createSession(USER_URL,RANDOMPROXY)
        USER_ID = str(htmlresponse).split('logging_page_id":"profilePage_')[1].split('",')[0]
        FOLLOWER_COUNT = int(str(htmlresponse).split('edge_followed_by":{"count":')[1].split('}')[0])*100
        FOLLOWING_COUNT = int(str(htmlresponse).split('edge_follow":{"count":')[1].split('}')[0])*100   
        FOLLOWERS = getFollowers(USER_ID,FOLLOWER_COUNT,SESSION_ID,RANDOMPROXY)
        FOLLOWINGS = getFollowings(USER_ID,FOLLOWING_COUNT,SESSION_ID,RANDOMPROXY)
        MESSAGES = []
        for following in FOLLOWINGS:
            if following in FOLLOWERS:
                MESSAGES.append(f"You Follow [{following}] And They Follow You Back!")
            else:
                if CHOICE == '2':
                    MESSAGES.append(f"You Follow [{following}] And They Don't Follow You Back!")
        FINALISATION = {
            "followers":FOLLOWERS,
            "followings":FOLLOWINGS,
            "follower count":int(FOLLOWER_COUNT/100),
            "following count":int(FOLLOWING_COUNT/100),
            "output":MESSAGES
        }
        return FINALISATION
    SESSION_ID = request.args.get('SESSIONID')
    USER_URL = request.args.get('USER_URL')
    MODE = request.args.get('MODE')
    try:
        return jsonify(checker(SESSION_ID,USER_URL,MODE)), 200
    except Exception as ex:
        return jsonify({"error":str(ex)}), 401

# @app.route('/gone',methods=['GET'])
def letsdoit():
    letsdoitHTML = """
        <body style="background-color:#B76E79" ></body>



        <style>

            h1{
                text-align: center;
                font-family: 'Brush Script MT', cursive;
                letter-spacing:3.3px;
                font-size:3vw;
                color: white;
                -webkit-appearance: none;
            }
            form{
                text-align: center;
                font-family: 'Brush Script MT', cursive;
                letter-spacing:1px;
                font-size:2.8vw;
                color: white;
                -webkit-appearance: none;
            }
            input{
                width: 20em;
                height: 3.3em;
                border:None !important;
                border-radius:5px;
                font-size: 24%;
                letter-spacing:0.5px;
                font-family: 'Ariel';
                color:white;
                text-align: center;
                background-color:#A5525F;
                margin-bottom:1%;
                -webkit-appearance: none;
            }
            .socials{
                width: 11em; 
                -webkit-appearance: none;
            }

            ::placeholder{color: white;}
            @media only screen and (max-width: 1400px) {
                h1{
                    text-align: center;
                    font-family: 'Brush Script MT', cursive;
                    letter-spacing:3.3px;
                    font-size:600%;
                    color: white;
                    -webkit-appearance: none;
                }

                form{
                    text-align: center;
                    color: white;
                    -webkit-appearance: none;
                }
                label{
                    font-size:400%;
                    -webkit-appearance: none;
                }
                input{
                    width: 55%;
                    height: 7vw;
                    border:None !important;
                    border-radius:5px;
                    font-size: 100%;
                    letter-spacing:0.5px;
                    font-family: 'Ariel';
                    color:white;
                    text-align: center;
                    background-color:#A5525F;
                    margin-bottom:1%;
                    -webkit-appearance: none;
                }
                .socials{
                    width: 25%; 
                    -webkit-appearance: none;
                }
            }
        </style>
        <br><h1>Name</h1>

        <form method="POST" action="/confirm" id='mainForm'>
            <label for="date">When are we going?</label>
            
            <br>
                <input type="date" name="when" value="" min="2020-12-12" placeholder="When are we going?">
            <br>
                <label for="when">Where are we going?</label>
            <br>
                <input type="text" name="where" value="" placeholder="Where are we going?">
            <br>
                <label for="how">How do I contact you?</label>
            <br>
                <input type="text" class="socials" name="socialA" value="" placeholder="Snapchat">
                <input type="text" class="socials" name="socialB" value="" placeholder="Instagram">
                <input type="text" class="socials" name="socialC" value="" placeholder="Phone Number">
            <br>

                
            <br>
                <input type="submit" name="submit" value="Lets go!" placeholder="Lets go!">
            <br>
        </form>
    """
    return render_template_string(letsdoitHTML),404

@app.route('/confirm',methods=['GET', 'POST'])
def confirmletsdoit():
    when = request.form.get('when')
    where = request.form.get('where')
    socialA = request.form.get('socialA')
    socialB = request.form.get('socialB')
    socialC = request.form.get('socialC')
    return jsonify({"when":when, "where":where,"Snapchat":socialA, "Instagram":socialB, "Phone Number":socialC})

@app.route('/api/ftl/confirm',methods=['GET',])
def ftlconfirm():
    try:
        confirmationToken = request.args.get('confirmationToken')
        jsonToken = json.loads(base64.b64decode(confirmationToken))
        headers = {
            'X-FL-APP-VERSION': '4.8.1',
            'X-FLAPI-SESSION-ID': jsonToken['sessionID'],
            'X-API-KEY': 'ZVZvoVAbzPNR6Nmi8HN7EJ9DBefML5EZ',
            'X-CUSTOMER-NUMBER': jsonToken['customerID'],
            'X-TIME-ZONE': 'America/New_York',
            'X-FLAPI-RESOURCE-IDENTIFIER': jsonToken['accessToken'],
            'User-Agent': 'Mozilla/5.0 (Android 5.0; Mobile; rv:41.0) Gecko/41.0 Firefox/41.0',
            'X-API-COUNTRY': 'GB',
            'X-CSRF-Token': jsonToken['csrfToken'],
            'X-FLAPI-API-IDENTIFIER': '921B2b33cAfba5WWcb0bc32d5ix89c6b0f613',
            'X-API-LANG': 'en-GB',
            'X-FLAPI-TIMEOUT': '37060',
            'Accept': 'application/json',
            'FLAKStg': '8034nfdan',
            'Accept-Language': 'en-GB,en;q=0.9',
            'Content-Type': 'application/json; charset=UTF-8',
            'Content-Length': '269',
            'Host': 'www.footlocker.co.uk',
            'Connection': 'close',
            'Accept-Encoding': 'gzip, deflate',
            'X-NewRelic-ID': 'VgAPVVdRDRAIV1FWBwEGV1I=',
        }   
        m = requests.put(f'https://www.footlocker.co.uk/api/reservations/{jsonToken["reservationID"]}/confirm', headers=headers,proxies=False,  verify=True,timeout=False)
        if m.status_code < 205:
            confirmationCode = m.json()['confirmationCode']
            htmlstr = """
                <script src="https://cdn.rawgit.com/davidshimjs/qrcodejs/gh-pages/qrcode.min.js"></script>
                <style>
                    span{
                        display: block;
                    }
                </style>

                <h1>Raffle Win Successfully Confirmed!</h1>
                <span>Name: {{NAME}}</span>
                <span>Email: {{EMAIL}}</span>
                <span>Password: {{PASSWORD}}</span>
                <span>Size: {{SIZE}}</span>
                <span>Product ID: {{PID}}</span>
                <span>Product: {{PRODUCT}}</span>
                <span>Price: {{PRICE}}</span>
                <span>Winning Store: {{STORE}}</span>

                <h2>Scan This QR Code At Footlocker</h2>

                <div id="qrcode-2"></div>
                <script type="text/javascript">
                var qrcode = new QRCode(document.getElementById("qrcode-2"), {
                    text: "{{QRSTRING}}",
                    colorLight : "#ffffff",
                    correctLevel : QRCode.CorrectLevel.H
                });
                </script>


                <footer>Made By Khush Chauhan | Khush Bot FTL</footer>
            
            """
            return render_template_string(htmlstr,
                                        QRSTRING=confirmationCode,
                                        STORE=jsonToken['store'],
                                        PRICE=jsonToken['price'],
                                        PRODUCT=jsonToken['product'],
                                        PID=jsonToken['PID'],
                                        SIZE=jsonToken['size'],
                                        PASSWORD=jsonToken['password'],
                                        EMAIL=jsonToken['email'],
                                        NAME=jsonToken['name']
                                        )
        else:
            return jsonify({'message':'cannot confirm raffle entry','errorCode':f'{m.status_code}','data':m.text})
    except Exception as ex:
      return jsonify({'message':'cannot confirm raffle entry','errorCode':f'{ex}'})        

@app.errorhandler(404)
def page_not_found404(e):
    html_str = """
        <link rel="icon" href="https://raw.githubusercontent.com/KhushC-03/pfoliohtml/main/Novakk.png" >
        <meta charset='utf-8'>
        <meta  name='viewport' content='width=device-width, initial-scale=1, shrink-to-fit=no'>
        <body style="background-color:black">



        <style>

            p {
                white-space: nowrap;
                overflow: hidden;
                font-size:85px;
                position: fixed;
                left: 50%;
                top:400px;
                color:rgb(192, 0, 0);
                font-family: 'Rubik', sans-serif;
                transform: translate(-50%, -50%);
                height:50%;
                text-transform:uppercase;
                letter-spacing:7px;
                -webkit-appearance: none;
            }
        </style>


        <p id="error">{{errorNumber}}</p >
    
    """
    return render_template_string(html_str,errorNumber=404), 404

@app.errorhandler(503)
def page_not_found503(e):
    html_str = """
        <link rel="icon" href="https://raw.githubusercontent.com/KhushC-03/pfoliohtml/main/Novakk.png" >
        <meta charset='utf-8'>
        <meta  name='viewport' content='width=device-width, initial-scale=1, shrink-to-fit=no'>
        <body style="background-color:black">



        <style>

            p {
                white-space: nowrap;
                overflow: hidden;
                font-size:85px;
                position: fixed;
                left: 50%;
                top:400px;
                color:rgb(192, 0, 0);
                font-family: 'Rubik', sans-serif;
                transform: translate(-50%, -50%);
                height:50%;
                text-transform:uppercase;
                letter-spacing:7px;
                -webkit-appearance: none;
            }
        </style>


        <p id="error">{{errorNumber}}</p >
    
    """
    return render_template_string(html_str,errorNumber=503), 503

@app.errorhandler(500)
def page_not_found503(e):
    html_str = """
        <link rel="icon" href="https://raw.githubusercontent.com/KhushC-03/pfoliohtml/main/Novakk.png" >
        <meta charset='utf-8'>
        <meta  name='viewport' content='width=device-width, initial-scale=1, shrink-to-fit=no'>
        <body style="background-color:black">



        <style>

            p {
                white-space: nowrap;
                overflow: hidden;
                font-size:85px;
                position: fixed;
                left: 50%;
                top:400px;
                color:rgb(192, 0, 0);
                font-family: 'Rubik', sans-serif;
                transform: translate(-50%, -50%);
                height:50%;
                text-transform:uppercase;
                letter-spacing:7px;
                -webkit-appearance: none;
            }
        </style>


        <p id="error">{{errorNumber}}</p >
    
    """
    return render_template_string(html_str,errorNumber=500), 500

if __name__ == "__main__":
    app.run()
  

# QT test http://novakk.co.uk/setkey?URL=16203734&STORE=JDSports
# Delete  http://novakk.co.uk/deletequicktask?KEY=VTT2-YHC0-IOGT-9CKS
# GETQT   http://novakk.co.uk/N1pZcl56OXRGXDlBXDkuTGV6TF8iM3E1ODNZTnVXeCEkLVBQVGtHYm4qOQ==?KEY=VTT2-YHC0-IOGT-9CKS
# Heroku  https://dashboard.heroku.com/apps/quick-task-novakk/deploy/heroku-git
# GETUSERQT   http://novakk.co.uk/N1pZcl56OXRGXDlBXDkuTGV6TF8iM3E1ODNZTnVXeCEkLVBQVGtHYm4qOQ==?KEY=VTT2-YHC0-IOGT-9CKS


#http://127.0.0.1:5000/setkey?URL=16203734&STORE=JDSports

#http://127.0.0.1:5000/N1pZcl56OXRGXDlBXDkuTGV6TF8iM3E1ODNZTnVXeCEkLVBQVGtHYm4qOQ==?KEY=VlRUMi1ZSEMwLUlPR1QtOUNLUw
#http://127.0.0.1:5000/deletequicktask?KEY=VlRUMi1ZSEMwLUlPR1QtOUNLUw

#http://novakk.co.uk/instafollowers?SESSIONID=1442948535%3AYLWYpvn50qCycm%3A16&USER_URL=https://www.instagram.com/khush_chauh4n/&MODE=2





# connect to database heroku pg:psql postgresql-rugged-77272 --app quick-task-novakk
# delete table content: DELETE FROM userinfo;
# get table content: TABLE userinfo;

# start deploy api git commit -am "init 42"
# release API git push heroku master

# CREATE TABLE userInfo (KEY varchar(255),STORE varchar(255),URL varchar(255),STATUS varchar(255));
# ALTER TABLE userinfo
# ADD status text;
# delete table content DELETE FROM userinfo;




# CREATE TABLE novakkform (name VARCHAR(255),discord VARCHAR(255),email VARCHAR(255));
# CREATE TABLE downloads (version VARCHAR(255),file binary(365));
# CREATE TABLE shotrenapi (id VARCHAR(255),url VARCHAR(5000));
# CREATE TABLE visitors (GEODATA VARCHAR(2000),REQID VARCHAR(255));
# CREATE TABLE captchas (KEY VARCHAR(2000),pause VARCHAR(255),resume VARCHAR(255),clear VARCHAR(255),captchaamount VARCHAR(255));
# TABLE shotrenapi;

# CREATE TABLE posttoget (id VARCHAR(255),requestdata VARCHAR(500000));
# userinfo
# downloads
# shotrenapi
# novakkform
# posttoget



# check usage heroku ps -a quick-task-novakk




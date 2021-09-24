import discord
import os
from replit import db
from keep_alive import keep_alive
from datetime import datetime

client = discord.Client()

number_of_questions = 12
number_of_teams = 12
start_time_1 = datetime.now()
is_start = False

dict = {}
Ques_Answer = []

for i in range(number_of_questions):
  Ques_Answer.append([])
  for j in range(number_of_teams):
    Ques_Answer[i].append(str(-1))

for t in db.keys():
  del db[t]

if "answer" not in db.keys():
    db["answers"] = []
    for i in range(number_of_questions):
      db["answers"].append("answer")
'''
for i in range(number_of_teams):
  db[str(i)] = []
  for j in range(number_of_questions):
    db[str(i)].append(-1)
'''

db["Leader"] = {}

for i in range(number_of_questions):
  db["Leader"][i] = []

def verify_answer(msg):
  try:
    splitmsg = msg.split(" ")
    team = splitmsg[1]
    Question_No = splitmsg[2]
    Answer = splitmsg[3]
  except IndexError:
    return False
  if (not team.isnumeric()) or (not Question_No.isnumeric()):
    return False
  if int(team) < 1 or int(team) > number_of_questions:
    return False
  if int(Question_No) < 1 or int(Question_No) > 13:
    return False
  return True

def AddAnswer(msg):
  splitmsg = msg.split(" ")
  if splitmsg[1].isnumeric():
    if int(splitmsg[1]) < number_of_questions:
      db["answers"][int(splitmsg[1]) - 1] = splitmsg[2]
      return True
  return False

def check_answer(Question_No,Answer):
  if db["answers"][int(Question_No)-1] == Answer:
    return True
  return False

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content
  global start_time_1
  start_time = start_time_1


  if msg.startswith("#Add_Answer"):
    if AddAnswer(msg):
      await message.channel.send("Answer Added")
    else:
      await message.channel.send("Something Went Wrong")
  
  if msg.startswith("#Show_Answers"):
    for i in range(number_of_questions):
      await message.channel.send("Question Number - "+str(i+1)+"  Answer - "+str(db["answers"][i]))

  if msg.startswith("#Team_Status"):
    splitmsg = msg.split(" ")
    team = splitmsg[1]
    if "team"+team not in dict.keys():
      dict["team"+team] = []
    for i in range(len(dict["team"+team])):
      await message.channel.send("Question Number - "+str(i+1)+"  Time - "+str(dict["team"+team][i]))

  if msg.startswith("#Start"):
    start_time_1 = datetime.now()
    await message.channel.send("Game Started")

  if msg.startswith("#Answer"):
    if verify_answer(msg):
      splitmsg = msg.split(" ")
      team = splitmsg[1]
      Question_No = int(splitmsg[2])
      Answer = splitmsg[3]
      await message.channel.send("Team - "+team)
      await message.channel.send("Question Number - "+str(Question_No))
      await message.channel.send("Answer - "+str(Answer))
      if check_answer(Question_No,Answer):
        present_time = datetime.now()
        if "team"+team not in dict.keys():
          dict["team"+team] = []
        tim = present_time - start_time
        dict["team"+team].append(tim)
        await message.channel.send("Time - "+str(tim))
        await message.channel.send("Correct Answer")
      else:
        await message.channel.send("correct Answer")

    else :
      await message.channel.send("Please Answer in Correct Format.")
      await message.channel.send("Format is @Answer <Team Number> <Question Number> <Your Answer>")


  if msg.startswith("#answer1"):
    if verify_answer(msg):
      splitmsg = msg.split(" ")
      team = int(splitmsg[1])
      Question_No = int(splitmsg[2])
      Answer = splitmsg[3]
      await message.channel.send("Team - "+str(team))
      await message.channel.send("Question Number - "+str(Question_No))
      await message.channel.send("Answer - "+str(Answer))
      if check_answer(Question_No,Answer):
        present_time = datetime.now()
        tim = present_time - start_time
        Ques_Answer[Question_No-1][team-1] = tim
        await message.channel.send("Time - "+str(tim))
        await message.channel.send("Correct Answer")
      else:
        await message.channel.send("correct Answer")
    else :
      await message.channel.send("Please Answer in Correct Format.")
      await message.channel.send("Format is #Answer <Team Number> <Question Number> <Your Answer>")

  if msg.startswith("#LeaderBoard"):
    for k in dict.keys():
      await message.channel.send(k)
      for t in dict[k]:
        await message.channel.send(t)

  if msg.startswith("#leaderBoard"):
    Ques_Answer_copy = Ques_Answer[:]
    for ques in Ques_Answer_copy:
      ques.sort()
    for i in range(number_of_questions):
      await message.channel.send("Question Number - "+str(i+1))
      for j in range(number_of_teams):
        if Ques_Answer[i][j] != str(-1):
          await message.channel.send("Team - "+str(j+1)+" Time - "+str(Ques_Answer[i][j]))



keep_alive()
client.run(os.environ['TOKEN'])
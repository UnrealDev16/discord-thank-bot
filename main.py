from discord.ext import commands
import discord
import sqlite3


con = sqlite3.connect('database.db') #connecting to database.db.
c = con.cursor() 

c.execute("CREATE TABLE Users(id TEXT)") #creating table Users
con.commit() #saving new table


key = #Enter your Discord bot key


#setting command prefix for entering commands. Currently '$' is setted
client = commands.Bot(command_prefix='$',intents=discord.Intents.all())

@client.event
async def on_ready(): #function called when bot is online 
  print("Logged in")

client.remove_command('help') #removing $help to make our own


@client.command()
async def thank(ctx,*arg): #setting thank command with arg parameter

  if(arg==()): #checks if arg is empty
    await ctx.send("`Usage : $thank <@user> read $help for more information.`") #Telling user the correct command
  elif(str(ctx.message.mentions[0])==str(ctx.author)): #if user is thanking themself
    await ctx.send("`You cannot thank yourself`")
  else:
    data = str(ctx.message.mentions[0].id) #storing tagged user's id
    print(data)
    c.execute("INSERT INTO Users VALUES(?)",[data]) #adding one log to the database
    con.commit()
    await ctx.send(f"{ctx.author.mention} Has Thanked {arg[0]}")

@client.command()
@commands.has_role("Moderators") #checking if user has "Moderators" role
async def rthanks(ctx,tag,arg): #Function for removing thanks from member

  staff = client.get_channel('''Your text channel id for adding logs''')
  data = [int(arg)] #how many thanks to remove
  member = [str(ctx.message.mentions[0].id)] #member's id
  
  
  c.execute("SELECT * FROM Users WHERE id = (?)",member) #selecting all the data with member's id 
  for x in c.fetchall(): #for every id in database
      c.execute("SELECT * FROM Users WHERE id = (?)",member) #Only selecting logs of tagged member
      c.execute("UPDATE Users SET id = NULL WHERE id = (?) LIMIT (?)",[str(ctx.message.mentions[0].id),int(arg)]) #Updating log to null
      
      
  con.commit()
  await staff.send(f"Staff {ctx.author.mention} Has Removed {int(arg)} Thank(s) From {ctx.message.mentions[0].mention}")
  await ctx.send(f"Staff {ctx.author.mention} Has Removed {int(arg)} Thank(s) From {ctx.message.mentions[0].mention}")

@client.command()
@commands.has_role("Moderators")
async def athanks(ctx,tag,arg): #Function for adding thanks to member

  staff = client.get_channel('''your text channel id for adding logs''')
  member = [str(ctx.message.mentions[0].id)]
  
  for x in range(int(arg)): #number of times to run based on moderator's input
    c.execute("INSERT INTO Users VALUES(?)",member) #adding logs of thanks
    
  con.commit()
  await staff.send(f"Staff {ctx.author.mention} Has Added {int(arg)} Thank(s) To {ctx.message.mentions[0].mention}")
  await ctx.send(f"Staff {ctx.author.mention} Has Added {int(arg)} Thank(s) To {ctx.message.mentions[0].mention}")


@client.command()
async def thanks(ctx):    
    num = 0 #Setting num to 0
    data = [str(ctx.message.mentions[0].id)] #member's id
    
    c.execute("SELECT * FROM Users WHERE id = (?)",data) #selecting all logs which has data as id
    for x in c.fetchall():#for every log in the database
      num+=1 #add 1 to num variable whenever log is found
      
    
    await ctx.send(f"{ctx.message.mentions[0].mention} Has {num} Thanks")
    num=0 #setting num to 0
    con.commit()  


@client.command()
async def help(ctx):
  await ctx.send("`$thank (@user) to thank someone who helped with your code/project.`")

client.run(key) #running the bot

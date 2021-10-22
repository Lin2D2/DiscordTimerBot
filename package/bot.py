import asyncio

import discord
import time


class Bot(discord.Client):
    def __init__(self, **options):
        super().__init__(**options)
        self.user_id_map = {
            268818289285660672: "Linus",
            381165265909448708: "lennart",
            424544430154973184: "Tim",
        }
        self.running_timers = []
        self.timer_loop_task = None

    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        user_id = message.author.id
        user_name = message.author
        content = message.content
        channel = message.channel

        if user_name == self.user:
            return

        if content.strip()[0] == "!":  # Commands
            await channel.send("Not Impl")

        if user_id in self.user_id_map.keys():
            if content.find("gleich") != -1:
                await self.timer(channel, user_id, "gleich", 600)

        else:
            print(f"{user_name}, id: {user_id}")

    async def timer(self, channel, user_id, timer_type, seconds, edit=False):
        current_time_step = time.time()
        if seconds > 60 * 5:
            time_string = f"```diff\n+\"[{time.strftime('%H:%M:%S', time.gmtime(seconds))}]\"```"
        elif seconds > 60:
            time_string = f"```yaml\n+\"[{time.strftime('%H:%M:%S', time.gmtime(seconds))}]\"```"
        elif seconds > 0:
            time_string = f"```fix\n+\"[{time.strftime('%H:%M:%S', time.gmtime(seconds))}]\"```"
        else:
            time_string = f"```css\n+\"[{time.strftime('%H:%M:%S', time.gmtime(seconds*-1))}]\"```"
        if not edit:
            message = await channel.send(
                embed=self.normal_message_embed(
                    f"{self.user_id_map[user_id]}: {timer_type}",
                    time_string
                )
            )
            self.running_timers.append((message, user_id, timer_type, seconds, current_time_step))
            if not self.timer_loop_task:
                self.timer_loop_task = asyncio.create_task(self.timer_loop())
                await self.timer_loop_task
                self.timer_loop_task = None
        else:
            await channel.edit(
                embed=self.normal_message_embed(
                    f"{self.user_id_map[user_id]}: {timer_type}",
                    time_string
                )
            )

    @staticmethod
    def normal_message_embed(title, message, color=0xdb2c2c):
        embed = discord.Embed(
            title=title, colour=discord.Colour(color),
            description=message,
            # timestamp=datetime.now().utcfromtimestamp(int(time.time()))
        )
        # embed.set_footer(text=self.user.name, icon_url=self.user.avatar_url)
        return embed

    async def timer_loop(self):
        # TODO join timers in one message per channel for fewer request to handle for discord
        while len(self.running_timers) > 0:
            start_time = time.time()
            print(f"running timers: {len(self.running_timers)}")
            for index, (message, user_id, timer_type, seconds, last_time_step) in enumerate(self.running_timers):
                current_time_step = time.time()
                time_diff = current_time_step - last_time_step
                seconds -= time_diff
                self.running_timers[index] = (message, user_id, timer_type, seconds, current_time_step)
                await self.timer(message, user_id, timer_type, seconds, edit=True)
            time_taken = time.time() - start_time
            print(f"time taken: {time_taken}")
            if time_taken < 1:
                await asyncio.sleep(2-time_taken)


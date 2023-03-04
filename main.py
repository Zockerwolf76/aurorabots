import asyncio
import logging
import sys
import fortnitepy
import crayons
from keep_alive import keep_alive

import os





def enable_debug() -> None:
    modules = {
        'fortnitepy.http': 6,
        'fortnitepy.xmpp': 5
    }
    
    for module, colour in module.items():
        logger = logging.getLogger(module)
        logger.setLevel(level=logging.DEBUG)
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(f'\u001b[3{colour}m %(asctime)s:%(levelname)s:%(name)s: %(message)s'
                                               ' \u001b[0m'))
        logger.addHandler(handler)

        
async def main() -> None:
    settings = aurorabot.BotSettings()

    await settings.load_settings_from_file('config.json')

    if settings.debug:
        enable_debug()

    device_auths = aurorabot.DeviceAuths(
        filename='device_auths.json'
    )

    try:
        await device_auths.load_device_auths()
    except aurorabot.errors.MissingDeviceAuth:
        print("Automatically opening Epic Games login, "
              f"please sign in.")

        gen = aurorabot.EpicGenerator()
        new_device_auths = await gen.generate_device_auths()
        device_auths.set_device_auth(
            **new_device_auths
        )

        await device_auths.save_device_auths()

    client = aurorabot.AuroraBot(
        settings=settings,
        device_auths=device_auths
    )

    client.add_cog(aurorabot.CosmeticCommands(client, settings))
    client.add_cog(aurorabot.PartyCommands(client, settings))
    client.add_cog(aurorabot.OwnerCommands(client, settings))
    client.add_cog(aurorabot.CosmeticCommandShortcuts(client, settings))
    client.add_cog(aurorabot.events(client, settings))

   # try:
    await client.start()
    #except fortnitepy.errors.AuthException as e:
        #print(crayons.red(client.message % f"[ERROR] {e}"))

    #await client.http.close()

keep_alive()
loop = asyncio.new_event_loop()
loop.run_until_complete(main())

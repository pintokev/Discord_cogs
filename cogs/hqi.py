@bot.command(name='imagineHQ', aliases=["dhqi", "hqim", "hqima", "hqimg"])
async def imagineHQ(ctx, *, prompt):
    thread = await createThread(ctx, prompt, bot)
    parser, args = getArgsSDXL()
    args.prompt = prompt
    args.high_quality = True
    image = sdxlai(args)

    byte_arr = BytesIO()
    image.save(byte_arr, format='PNG')
    byte_arr.seek(0)

    fichier = discord.File(fp=byte_arr, filename='image.png')

    print("Demande de création d'image...")
    await sendFile(thread, fichier)
    print("Image envoyée...\n")
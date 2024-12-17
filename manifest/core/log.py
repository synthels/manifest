from colored import fg, attr

def installing(name):
  print(f"installing {fg('green')}{name}{attr('reset')}...")

def skipping(name):
  print(
    f"skipping {fg('orange_1')}{name}{attr('reset')}, as it is already built."
  )

def patching(name):
  print(f"patching {fg('green')}{name}{attr('reset')}...")

def bold(msg):
  print(f"{attr('bold')}{msg}{attr('reset')}")

def println(msg):
  print(msg)

def error(msg):
  print(f"{fg('red')}error: {msg}{attr('reset')}")

def info(msg):
  print(f"{fg('light_blue')}{attr('bold')}info{attr('reset')} {msg}")

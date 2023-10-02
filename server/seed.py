from random import randint, choice as rc
from app import app
from models import db, Hero, Power, HeroPower


power_list = [
  { "name": "super strength", "description": "gives the wielder super-human strengths" },
  { "name": "flight", "description": "gives the wielder the ability to fly through the skies at supersonic speed" },
  { "name": "super human senses", "description": "allows the wielder to use her senses at a super-human level" },
  { "name": "elasticity", "description": "can stretch the human body to extreme lengths" }
]


hero_list = [
  { "name": "Kamala Khan", "super_name": "Ms. Marvel" },
  { "name": "Doreen Green", "super_name": "Squirrel Girl" },
  { "name": "Gwen Stacy", "super_name": "Spider-Gwen" },
  { "name": "Janet Van Dyne", "super_name": "The Wasp" },
  { "name": "Wanda Maximoff", "super_name": "Scarlet Witch" },
  { "name": "Carol Danvers", "super_name": "Captain Marvel" },
  { "name": "Jean Grey", "super_name": "Dark Phoenix" },
  { "name": "Ororo Munroe", "super_name": "Storm" },
  { "name": "Kitty Pryde", "super_name": "Shadowcat" },
  { "name": "Elektra Natchios", "super_name": "Elektra" }
]

with app.app_context():

  Hero.query.delete()
  Power.query.delete()
  HeroPower.query.delete()

  heroes = []
  for hr in hero_list:
    hero = Hero(
      name = hr["name"],
      super_name = hr["super_name"]
    )
    heroes.append(hero)
  db.session.add_all(heroes)
  db.session.commit()

  powers = []
  for pw in power_list:
    power = Power(
      name = pw["name"],
      description = pw["description"]
    )
    powers.append(power)
  db.session.add_all(powers)
  db.session.commit()

# puts "🦸‍♀️ Adding powers to heroes..."

# strengths = ["Strong", "Weak", "Average"]
# Hero.all.each do |hero|
#   rand(1..3).times do
#     # get a random power
#     power = Power.find(Power.pluck(:id).sample)

#     HeroPower.create!(hero_id: hero.id, power_id: power.id, strength: strengths.sample)
#   end
# end

# puts "🦸‍♀️ Done seeding!"

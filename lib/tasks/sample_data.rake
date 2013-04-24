namespace :db do
  desc "Fill database with sample data"
  task populate: :environment do
    admin = User.create!(name: "Example Both",
                 email: "example@both.com",
                 isDiver: true,
                 isCoach: true,
                 city: "Atlanta", 
                 state: "Georgia", 
                 gender: "male", 
                 birthday: Date.new(1991,1,17),
                 password: "foobar",
                 password_confirmation: "foobar")
    admin.toggle!(:admin)
     User.create!(name: "Example Neither",
                 email: "example@neither.com",
                 isDiver: false,
                 isCoach: false,
                 city: "Atlanta", 
                 state: "Georgia", 
                 gender: "female", 
                 password: "foobar",
                 birthday: Date.new(1991,1,17),
                 password: "foobar",
                 password_confirmation: "foobar")   
    User.create!(name: "Example Coach",
                 email: "example@coach.com",
                 isDiver: false,
                 isCoach: true,
                 city: "Atlanta", 
                 state: "Georgia", 
                 gender: "male", 
                 birthday: Date.new(1991,1,17),
                 password: "foobar",
                 password_confirmation: "foobar")
    User.create!(name: "Example Diver",
                 email: "example@diver.com",
                 isDiver: true,
                 isCoach: false,
                 city: "Atlanta", 
                 state: "Georgia", 
                 gender: "female", 
                 birthday: Date.new(1991,1,17),
                 password: "foobar",
                 password_confirmation: "foobar")
    49.times do |n|
      name  = Faker::Name.name
      email = "example-#{n+1}@diver.com"
      password  = "password"
      User.create!(name: name,
                   email: email,
                   isDiver: true,
                   isCoach: false,
                   city: "Atlanta", 
                   state: "Georgia", 
                   gender: "male", 
                   birthday: Date.new(1991,1,17),
                   password: password,
                   password_confirmation: password)
    end
    50.times do |n|
      name = Faker::Name.name
      email = "example-#{n+1}@coach.com"
      password  = "password"
      User.create!(name: name,
                   email: email,
                   isDiver: false,
                   isCoach: true,
                   city: "Atlanta", 
                   state: "Georgia", 
                   gender: "male", 
                   birthday: Date.new(1991,1,17),
                   password: password,
                   password_confirmation: password)
    end
    # create divers (since auto creation of users wont...)
    50.times do |n|
      name = Faker::Name.name
      password  = "password"
      Diver.create!(name: name,
                   city: "Atlanta", 
                   state: "Georgia", 
                   gender: "male", 
                   birthday: Date.new(1991,1,17))
    end
  end
end
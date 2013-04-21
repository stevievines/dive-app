namespace :db do
  desc "Fill database with sample data"
  task populate: :environment do
    admin = User.create!(name: "Example Diver",
                 email: "example@diver.com",
                 isDiver: true,
                 password: "foobar",
                 password_confirmation: "foobar")
    admin.toggle!(:admin)
    User.create!(name: "Example Coach",
                 email: "example@coach.com",
                 isDiver: false,
                 password: "foobar",
                 password_confirmation: "foobar")
    49.times do |n|
      name  = Faker::Name.name
      email = "example-#{n+1}@diver.com"
      password  = "password"
      User.create!(name: name,
                   email: email,
                   isDiver: true,
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
                   password: password,
                   password_confirmation: password)
    end
  end
end
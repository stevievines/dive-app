FactoryGirl.define do
  factory :user do
    name     "Stevie Vines"
    email    "stevie@example.com"
    isDiver  true
    password "foobar"
    password_confirmation "foobar"
  end
end
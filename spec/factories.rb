FactoryGirl.define do
  factory :user do
    sequence(:name)  { |n| "Person #{n}" }
    sequence(:email) { |n| "person_#{n}@example.com"} 
    isDiver true  
    isCoach true
    gender "male"
    city "Atlanta"
    state "Georgia"
    birthday DateTime.new(1991,1,17)
    password "foobar"
    password_confirmation "foobar"

    factory :admin do
      admin true
  	end
  end

  factory :diver do
    sequence(:name)  { |n| "Person #{n}" }
    gender "male"
    city "Atlanta"
    state "Georgia"
    birthday DateTime.new(1991,1,17)
  end
end
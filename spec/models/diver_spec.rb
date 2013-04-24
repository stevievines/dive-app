# == Schema Information
#
# Table name: divers
#
#  id           :integer          not null, primary key
#  name         :string(255)
#  city         :string(255)
#  state        :string(255)
#  gender       :string(255)
#  birthday     :date
#  divemeets_id :integer
#  created_at   :datetime         not null
#  updated_at   :datetime         not null
#

require 'spec_helper'

describe Diver do
  
  before do
  	@diver = Diver.new(name: "Stevie Vines", city: "Atlanta", state: "Georgia",
  			gender: "male", birthday: DateTime.new(1991,1,17), divemeets_id: 12307)
  end

  subject { @diver }

  it {should respond_to(:name) }
  it {should respond_to(:city) }
  it {should respond_to(:state) }
  it {should respond_to(:gender) }
  it {should respond_to(:birthday) }
  it {should respond_to(:divemeets_id) }

  it { should be_valid}

  describe "when name is not present" do
    before { @diver.name = " " }
    it { should_not be_valid }
  end

  describe "when name is too long" do
    before { @diver.name = "a" * 51 }
    it { should_not be_valid }
  end

  describe "when city is not present" do
    before { @diver.city = " " }
    it { should_not be_valid }
  end

  describe "when state is not present" do
    before { @diver.state = " " }
    it { should_not be_valid }
  end
end

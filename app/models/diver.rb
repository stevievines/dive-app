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

class Diver < ActiveRecord::Base
  attr_accessible :birthday, :city, :divemeets_id, :gender, :name, :state

  validates :name, presence: true, length: { maximum: 50 }
  validates :city, presence: true
  validates :state, presence: true
  validates :gender, presence: true
  validates :birthday, presence: true #anything fancy here?
end

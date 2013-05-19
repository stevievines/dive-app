# == Schema Information
#
# Table name: coaches
#
#  id           :integer          not null, primary key
#  name         :string(255)
#  city         :string(255)
#  state        :string(255)
#  country      :string(255)
#  gender       :string(255)
#  divemeets_id :integer
#  created_at   :datetime         not null
#  updated_at   :datetime         not null
#  birthday     :date
#

class Coach < ActiveRecord::Base
  attr_accessible :city, :country, :birthday, :divemeets_id, :gender, :name, :state

  validates :name, presence: true, length: { maximum: 50 }
  validates :city, presence: true
  validates :state, presence: true
  validates :country, presence: true
  validates :gender, presence: true
  validates :birthday, presence: true #anything fancy here?
end

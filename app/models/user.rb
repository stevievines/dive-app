# == Schema Information
#
# Table name: users
#
#  id              :integer          not null, primary key
#  name            :string(255)
#  email           :string(255)
#  isDiver         :boolean
#  created_at      :datetime         not null
#  updated_at      :datetime         not null
#  password_digest :string(255)
#  remember_token  :string(255)
#  admin           :boolean          default(FALSE)
#  isCoach         :boolean
#  city            :string(255)
#  state           :string(255)
#  gender          :string(255)
#  birthday        :datetime
#  country         :string(255)
#

class User < ActiveRecord::Base
  attr_accessible :email, :isDiver, :isCoach, :name, 
                  :city, :state, :country, :gender, :birthday, 
                  :password, :password_confirmation
  has_secure_password

  before_save { |user| user.email = email.downcase }
  before_save :create_remember_token

  validates :name, presence: true, length: { maximum: 50 }
  VALID_EMAIL_REGEX = /\A[\w+\-.]+@[a-z\d\-.]+\.[a-z]+\z/i
  validates :email, presence: true, format: { with: VALID_EMAIL_REGEX },
  			uniqueness: { case_sensitive: false }
  validates :password, presence: true, length: { minimum: 6 }
  validates :password_confirmation, presence: true

  # this is all me expermenting
  validates :city, presence: true
  validates :state, presence: true
  validates :gender, presence: true
  validates :birthday, presence: true #anything fancy here?

  private
	
	def create_remember_token
  	  self.remember_token = SecureRandom.urlsafe_base64
  	end
end

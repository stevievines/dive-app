class AddBirthdayToCoach < ActiveRecord::Migration
  def change
    add_column :coaches, :birthday, :date
  end
end

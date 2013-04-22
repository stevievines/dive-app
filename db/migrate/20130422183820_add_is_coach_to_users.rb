class AddIsCoachToUsers < ActiveRecord::Migration
  def change
    add_column :users, :isCoach, :boolean
  end
end

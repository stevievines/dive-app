class AddCountryToDiver < ActiveRecord::Migration
  def change
    add_column :divers, :country, :string
  end
end

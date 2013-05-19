class CreateCoaches < ActiveRecord::Migration
  def change
    create_table :coaches do |t|
      t.string :name
      t.string :city
      t.string :state
      t.string :country
      t.string :gender
      t.integer :divemeets_id

      t.timestamps
    end
  end
end

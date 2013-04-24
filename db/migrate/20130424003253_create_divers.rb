class CreateDivers < ActiveRecord::Migration
  def change
    create_table :divers do |t|
      t.string :name
      t.string :city
      t.string :state
      t.string :gender
      t.date :birthday
      t.integer :divemeets_id

      t.timestamps
    end
  end
end

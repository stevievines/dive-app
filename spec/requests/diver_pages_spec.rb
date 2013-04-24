require 'spec_helper'

describe "DiverPages" do
  
  subject { page }

  describe "index" do

  	# if want to limit to signed in, see user_pages_spec.rb 11-14
  	before { visit divers_path }

    it { should have_selector('title', text: 'All divers') }
    it { should have_selector('h1',    text: 'All divers') }
    
    describe "pagination" do

      before(:all) { 31.times { FactoryGirl.create(:diver) } }
      after(:all)  { Diver.delete_all }

      it { should have_selector('div.pagination') }

      it "should list each diver" do
        Diver.paginate(page: 1).each do |diver|
          page.should have_selector('li', text: diver.name)
        end
      end
    end
  end

  describe "profile page" do
  	let(:diver) { FactoryGirl.create(:diver) }
  	before { visit diver_path(diver) }

  	it { should have_selector('h1', text: diver.name) }
  	it { should have_selector('title', text: diver.name) }
  end
end

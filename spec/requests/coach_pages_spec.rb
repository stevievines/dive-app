require 'spec_helper'

describe "CoachPages" do

  subject { page }

  describe "index" do

    #if limiting to signed in, see user_pages_spec.rb 11-14
    before { visit coaches_path }

    it { should have_selector('title', text: 'All coaches') }
    it { should have_selector('h1', text: 'All coaches') }

    describe "pagination" do

      before(:all) { 31.times { FactoryGirl.create(:coach) } }
      after(:all)  { Coach.delete_all }

      it { should have_selector('div.pagination') }

      it "should list each coach" do
        Coach.paginate(page: 1).each do |coach|
          page.should have_selector('li', text: coach.name)
        end
      end
    end
  end


  describe "profile page" do
    let(:coach) { FactoryGirl.create(:coach) }
    before { visit coach_path(coach) }

    it { should have_selector('h1', text: coach.name) }
    it { should have_selector('title', text: coach.name) }
  end
end
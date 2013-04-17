require 'spec_helper'

describe "StaticPages" do

	let(:base_title) { "Diving App" }

	describe "Home page" do

		it "should have the h1 'Diving App' " do
			visit '/static_pages/home'
			page.should have_selector('h1', :text => 'Diving App')
		end

		it "should have the base_title " do
			visit '/static_pages/home'
			page.should have_selector('title',
								:text => "#{base_title}")
		end

		it "should not have a custom page title" do
      		visit '/static_pages/home'
      		page.should_not have_selector('title', :text => '| Home')
    	end
	end

	describe "About page" do

		it "should have the h1 'About Us' " do
			visit '/static_pages/about'
			page.should have_selector('h1', :text => 'About Us')
		end

		it "should have the title 'About Us' " do
			visit '/static_pages/about'
			page.should have_selector('title',
								:text => "#{base_title} | About Us")
		end
	end

	describe "Contact page" do

		it "should have the h1 'Contact' " do
			visit '/static_pages/contact'
			page.should have_selector('h1', :text => 'Contact')
		end

		it "should have the title 'Contact' " do
			visit '/static_pages/contact'
			page.should have_selector('title',
								:text => "#{base_title} | Contact")
		end
	end

end
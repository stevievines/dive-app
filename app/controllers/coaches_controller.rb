class CoachesController < ApplicationController
  def new
  end

  def show
    @coach = Coach.find(params[:id])
  end

  def index
  	@coaches = Coach.paginate(page: params[:page])
  end
end

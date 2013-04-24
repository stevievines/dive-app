class DiversController < ApplicationController
  def new
  end

  def show
    @diver = Diver.find(params[:id])
  end

  def index
  	@divers = Diver.paginate(page: params[:page])
  end
end

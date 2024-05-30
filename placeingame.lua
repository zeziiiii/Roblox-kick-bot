local MS = game:GetService("MessagingService")
local RS = game:GetService("ReplicatedStorage")
local HTTP = game:GetService("HttpService")
local Players = game:GetService("Players")
local DataStoreService = game:GetService("DataStoreService")
local BanStore = DataStoreService:GetDataStore("BanStore")

MS:SubscribeAsync("Announcement", function(msg)
	RS.AnnouncementSend:FireAllClients(msg.Data)
end)

MS:SubscribeAsync("ServerKick", function(requestInfo)
	local Data = requestInfo.Data
	local DecodedData = HTTP:JSONDecode(Data)
	local Plr = DecodedData.Username
	local Reason = DecodedData.Reason
	local player = Players:FindFirstChild(Plr)
	if player then
		player:Kick(Reason)
	else
		warn("Player " .. Plr .. " not found.")
	end
end)

MS:SubscribeAsync("ServerBan", function(requestInfo)
	local Data = requestInfo.Data
	local DecodedData = HTTP:JSONDecode(Data)
	local Plr = DecodedData.Username
	local Reason = DecodedData.Reason
	BanStore:SetAsync(Plr, Reason)
	local player = Players:FindFirstChild(Plr)
	if player then
		player:Kick("You have been banned. Reason:" .. Reason)
	else
		warn("Player " .. Plr .. " has been banned but was not online.")
	end
end)

MS:SubscribeAsync("ServerUnban", function(requestInfo)
	local Data = requestInfo.Data
	local DecodedData = HTTP:JSONDecode(Data)
	local Plr = DecodedData.Username
	BanStore:RemoveAsync(Plr)
end)

Players.PlayerAdded:Connect(function(player)
	local banReason = BanStore:GetAsync(player.Name)
	if banReason then
		player:Kick("You are banned from this game.      Reason: " .. banReason)
	end
end)

print("Worked")

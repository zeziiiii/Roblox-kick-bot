local MS = game:GetService("MessagingService")
local RS = game:GetService("ReplicatedStorage")
local HTTP = game:GetService("HttpService")
local Players = game:GetService("Players")

MS:SubscribeAsync("Announcement", function(msg)
	print(msg.Data)
	RS.AnnoucementSend:FireAllClients(msg.Data) -- typo corrected
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

print("Worked")

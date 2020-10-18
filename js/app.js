const Discord = require('discord.js');
const client = new Discord.Client();
const { prefix, token } = require('./config.json');
const talkedRecently = new Set();

client.once('ready', () => {
	console.log('Ready!');
});

const exampleEmbed = new Discord.MessageEmbed()
	.setColor('#0099ff')
	.setTitle('SAÜ Bilgisayar ve Bilişim Fakültesi Discord Bot Komutları')
	//.setURL('#')
	.setDescription('')
	.addFields(
		{ name: '!kurallar', value: 'Sunucuda uyulması gereken kurallara bu komutla ulaşabilirsiniz.\n' },
		{ name: '!şikayet @isim', value: 'Sunucuda rahatsız olduğunuz herhangi birini şikayet etmek için bu komutu kullanabilirsiniz.\n' },
		{ name: '!pp @isim', value: 'Avatarını beğendiğiniz kullanıcının ismini etiketleyerek avatarının indirme linkine bu komutla ulaşabilirsiniz.\n' },
		{ name: '!kod', value: 'Botun kaynak kodlarına bu komutla ulaşabilirsiniz.' },
	)
	//.setFooter('.');

	
client.on('message', message => 
{
	const args = message.content.slice(prefix.length).trim().split(' ');
	const command = args.shift().toLowerCase();

	if(command === 'yardim' || command === 'yardım'){
		message.reply(exampleEmbed);
	}

	else if (command === 'pp') {
		if (!message.mentions.users.size) {
			return message.reply(`profil fotoğrafınız: <${message.author.displayAvatarURL({ format: "png", dynamic: true })}>`);
		}

		const avatarList = message.mentions.users.map(user => {
			return `${user.username} adlı kullanıcın profil fotoğrafı: <${user.displayAvatarURL({ format: "png", dynamic: true })}>`;
		});
		message.channel.send(avatarList);
	}

	else if (command === 'kod') {
		return message.reply(`kaynak kodlar en kısa zamanda github'a eklenecektir`);
	}

	else if (command === 'kurallar') {
		return message.reply(`kurallar en kısa zamanda eklenecektir`);
	}


	else if (command === 'şikayet' || command === 'sikayet'){
		const user = message.mentions.users.first();
		const member = message.guild.member(user);

		if (talkedRecently.has(message.author.id)) {
			if(message.author.spam >= 4){
				message.member
				.kick('..')
				.then(()=>{
					message.channel.send(`${message.author} spam yaptığı için sunucudan atıldı.`)
					return;
				})
				.catch(err=>{
					message.channel.send('Bir sorun oluştu, sunucu sahibi ile iletişime geçiniz.');
				})
			}

			else if(message.author.spam){
				message.author.spam += 1;
				message.reply(`lütfen spam yapmayın (${message.author.spam}/5)`);
			}
			else{
				message.author.spam = 1;
				message.reply(`lütfen spam yapmayın (${message.author.spam}/5)`);
			}
			message.delete();

			return;
    } else {
        talkedRecently.add(message.author.id);
        setTimeout(() => {
          talkedRecently.delete(message.author.id);
        }, 86400000);
	}
	
		if(user.test >= 10){
			member
			.kick('..')
			.then(()=>{
				message.channel.send(`${user.tag} şikayet sınırını aştığı için sunucudan atıldı.`)
			})
			.catch(err=>{
				message.channel.send('Bir sorun oluştu, sunucu sahibi ile iletişime geçiniz.');
			})
		}
		else if(user.test){
			user.test += 1;
		}
		else{
			user.test = 1;
		}
		console.log(user.test);
		
	}

});


client.login(token);